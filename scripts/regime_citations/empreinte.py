"""
L'empreinte canonique de l'ancien système (invariant A du régime des citations).

Lancer depuis la racine de l'arbre de travail à mesurer :

    PYTHONHASHSEED=0 PYTHONPATH=scripts/regime_citations \\
    DJANGO_SETTINGS_MODULE=settings_clone_regime \\
    python scripts/regime_citations/empreinte.py --base court_quote_regime_clone --sortie a.json

Sûretés : refuse de tourner sur une autre base que `--base` ; toute la mesure
tourne dans une transaction annulée, chaque surface dans un point de sauvegarde
annulé ; toute connexion réseau hors de la machine est refusée ; l'ordre des
ensembles Python doit être fixé (`PYTHONHASHSEED=0`).

Le script ne lit ni n'écrit le champ `regime` : il tourne tel quel avant et
après la migration. La projection est décrite dans le README.
"""
import argparse
import io
import os
import socket
import sys
import time
import zipfile
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import projection as P  # noqa: E402

BASE_REELLE = "court_project_pg"
_LOCAL = {"localhost", "127.0.0.1", "::1"}


def bloquer_reseau():
    connect = socket.socket.connect

    def garde(self, adresse):
        if isinstance(adresse, tuple) and adresse and adresse[0] not in _LOCAL:
            raise ConnectionRefusedError(f"réseau bloqué pendant l'empreinte : {adresse[0]}")
        return connect(self, adresse)

    socket.socket.connect = garde
    getaddrinfo = socket.getaddrinfo

    def garde_dns(hote, *a, **k):
        if hote is not None and hote not in _LOCAL:
            raise socket.gaierror(f"réseau bloqué pendant l'empreinte : {hote}")
        return getaddrinfo(hote, *a, **k)

    socket.getaddrinfo = garde_dns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="nom de la base attendue (garde)")
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--filtre", help="ne mesurer que les URL qui contiennent ce texte (contrôles ponctuels)")
    ap.add_argument("--sans-services", action="store_true")
    args = ap.parse_args()

    if os.environ.get("PYTHONHASHSEED") != "0":
        sys.exit("lancer avec PYTHONHASHSEED=0 : l'ordre des ensembles de chaînes en dépend")
    if args.base == BASE_REELLE:
        sys.exit("la base réelle n'est pas mesurée par ce script sans décision explicite")

    import django
    django.setup()
    from django.db import connection
    if connection.settings_dict["NAME"] != args.base:
        sys.exit(f"base connectée {connection.settings_dict['NAME']!r} ≠ --base {args.base!r}")
    bloquer_reseau()
    from django.test.utils import setup_test_environment
    setup_test_environment()

    Mesure(args).executer()


class Mesure:

    def __init__(self, args):
        from django.db.models import Model, QuerySet
        from django.db.models.signals import post_init

        from argument_manager.models import TrameNarrative
        from email_manager.models import Quote as EmailQuote
        from pdf_manager.models import Quote as PDFQuote

        self.args = args
        self.Model, self.QuerySet = Model, QuerySet
        self.suivis = {EmailQuote: "email_quote", PDFQuote: "pdf_quote", TrameNarrative: "trame"}
        self.vus = []
        self.actif = False

        def recepteur(sender, instance, **kwargs):
            if self.actif and instance.pk is not None:
                self.vus.append((self.suivis[sender], instance.pk))

        for modele in self.suivis:
            post_init.connect(recepteur, sender=modele, weak=False)

    # -- contexte de rendu -------------------------------------------------
    def _parcourir(self, valeur, ordre, presence, deja, profondeur=0, consomme=True):
        """Parcours en profondeur, dans l'ordre où la vue a remis les objets au
        gabarit. `presence` reçoit toute citation rencontrée ; `ordre` seulement
        celles d'une collection que la surface a consommée, à leur première
        rencontre.

        Une collection est consommée quand la vue ou le gabarit l'a évaluée. Un
        QuerySet resté non évalué après le rendu n'a été ni affiché ni utilisé :
        l'instrument l'évalue pour en contrôler la présence et le contenu, mais
        l'ordre que la base lui donne alors n'est pas un comportement de la
        surface (README, « La projection », troisième sorte)."""
        from collections.abc import ItemsView, KeysView, ValuesView
        if profondeur > 7 or valeur is None or isinstance(valeur, (str, bytes, int, float, bool)):
            return
        if id(valeur) in deja:
            return
        deja.add(id(valeur))
        rec = lambda v: self._parcourir(v, ordre, presence, deja, profondeur + 1, consomme)  # noqa: E731
        if isinstance(valeur, self.Model):
            label = self.suivis.get(type(valeur))
            if label and valeur.pk is not None:
                presence.add((label, valeur.pk))
                if consomme and (label, valeur.pk) not in ordre:
                    ordre.append((label, valeur.pk))
            for v in (getattr(valeur, "_prefetched_objects_cache", None) or {}).values():
                rec(v)
            return
        if isinstance(valeur, self.QuerySet):
            if valeur._result_cache is not None:
                for v in list(valeur):
                    rec(v)
            elif valeur.model in self.suivis:
                for v in list(valeur):  # non consommé : présence et contenu seulement
                    self._parcourir(v, ordre, presence, deja, profondeur + 1, consomme=False)
            return
        if isinstance(valeur, dict):
            for v in valeur.values():
                rec(v)
            return
        if isinstance(valeur, (set, frozenset)):
            # un ensemble Python n'a pas d'ordre : on le parcourt trié
            for v in sorted(valeur, key=lambda x: P.canon(str(x))):
                rec(v)
            return
        if isinstance(valeur, (list, tuple, ItemsView, KeysView, ValuesView)):
            for v in valeur:
                rec(v)
            return
        champs = getattr(valeur, "fields", None)
        if isinstance(champs, dict):
            for champ in champs.values():
                qs = getattr(champ, "queryset", None)
                if isinstance(qs, self.QuerySet):
                    rec(qs)
        attributs = getattr(valeur, "__dict__", None)
        if isinstance(attributs, dict) and type(valeur).__module__.split(".")[0] in {
            "argument_manager", "case_manager", "core", "document_manager",
            "email_manager", "pdf_manager", "protagonist_manager", "events",
        }:
            rec(attributs)

    def _contexte(self, reponse):
        """(ordre des collections consommées, présence de toutes les citations)."""
        ctx = getattr(reponse, "context", None)
        ordre, presence, deja = [], set(), set()
        if ctx is None:
            return ordre, presence
        for c in (ctx if isinstance(ctx, list) else [ctx]):
            try:
                plat = c.flatten()
            except Exception:
                plat = c if isinstance(c, dict) else {}
            self._parcourir(plat, ordre, presence, deja)
        return ordre, presence

    # -- une surface -------------------------------------------------------
    def _existe(self, label, pk):
        from django.apps import apps
        return apps.get_model(label)._base_manager.filter(pk=pk).exists()

    def projeter(self, url, reponse, vus):
        ctype = reponse.get("Content-Type", "").split(";")[0]
        ordre_ctx, presence_ctx = self._contexte(reponse)
        proj = {
            "url": url,
            "statut": reponse.status_code,
            "type": ctype,
            # ENSEMBLES : présence
            "ens_instanciees": P.ensemble(f"{l}:{pk}" for l, pk in vus),
            "ens_contexte": P.ensemble(f"{l}:{pk}" for l, pk in presence_ctx),
            "nb_instanciations": dict(sorted(_compter(l for l, _ in vus).items())),
            # SÉQUENCES : ordre observable
            "seq_contexte": P.sequence(f"{l}:{pk}" for l, pk in ordre_ctx),
        }
        secondaire = {}
        corps = b"".join(reponse.streaming_content) if getattr(reponse, "streaming", False) else reponse.content
        if "json" in ctype:
            import json
            try:
                proj["json"] = P.empreinte(json.loads(corps))   # listes JSON : séquences
            except ValueError:
                proj["json"] = "illisible:" + P.empreinte(corps.decode("utf-8", "replace"))
        if "html" in ctype or "json" in ctype:
            texte = corps.decode("utf-8", "replace")
            proj["seq_marqueurs"] = P.marqueurs(texte)
            if "html" in ctype and reponse.status_code < 500:
                # hors pages d'erreur : la trace de débogage porte des adresses mémoire
                secondaire["html"] = P.empreinte(" ".join(P.normaliser_texte(texte).split()))
        elif ctype.startswith("text/"):
            proj["texte"] = P.empreinte(P.normaliser_texte(corps.decode("utf-8", "replace")))
        elif ctype.endswith("wordprocessingml.document"):
            proj["docx_texte"] = _texte_docx(corps)
        else:
            proj["longueur"] = len(corps)
        return proj, secondaire

    # -- surfaces ----------------------------------------------------------
    def executer(self):
        from django.contrib.auth import get_user_model
        from django.db import connection, reset_queries, transaction
        from django.test import Client

        import surfaces as S

        t0 = time.time()
        utilisateur = get_user_model()._base_manager.filter(is_superuser=True, is_active=True).order_by("pk").first()
        assert utilisateur, "aucun superutilisateur actif"
        sortie = {"surfaces": {}, "secondaire": {}, "services": {}}
        with transaction.atomic():
            client = Client(raise_request_exception=False)
            client.force_login(utilisateur)
            liste = S.surfaces()
            sortie["liste_des_surfaces"] = P.empreinte(liste)
            if self.args.filtre:
                liste = [u for u in liste if self.args.filtre in u]
            for i, url in enumerate(liste):
                point = transaction.savepoint()
                self.vus = []
                self.actif = True
                location = None
                try:
                    rep = client.get(url)
                    self.actif = False
                    proj, sec = self.projeter(url, rep, list(self.vus))
                    location = rep.get("Location")
                except Exception as e:  # noqa: BLE001
                    self.actif = False
                    proj, sec = {"url": url, "erreur": f"{type(e).__name__}: {e}"}, {}
                finally:
                    transaction.savepoint_rollback(point)
                    reset_queries()
                # après l'annulation : une PK de redirection qui n'existe plus était temporaire
                proj["location"] = P.normaliser_location(location, self._existe)
                sortie["surfaces"][url] = proj
                sortie["secondaire"][url] = sec
                if i % 500 == 0:
                    print(f"  {i}/{len(liste)} ({time.time() - t0:.0f} s)", file=sys.stderr)
            if not self.args.sans_services:
                sortie["services"] = self.services()
            transaction.set_rollback(True)

        sortie["empreintes"] = {
            "surfaces": P.empreinte(sortie["surfaces"]),
            "services": P.empreinte(sortie["services"]),
            "secondaire": P.empreinte(sortie["secondaire"]),
        }
        sortie["empreintes"]["canonique"] = P.empreinte([sortie["empreintes"]["surfaces"],
                                                         sortie["empreintes"]["services"]])
        statuts = _compter(str(p.get("statut", "erreur")) for p in sortie["surfaces"].values())
        sortie["meta"] = {"base": connection.settings_dict["NAME"], "arbre": os.getcwd(),
                          "surfaces": len(sortie["surfaces"]), "secondes": round(time.time() - t0, 1),
                          "statuts": dict(sorted(statuts.items()))}
        import json
        with open(self.args.sortie, "w", encoding="utf-8") as fh:
            json.dump(sortie, fh, ensure_ascii=False, indent=1, sort_keys=True, default=str)
        print(json.dumps({"empreintes": sortie["empreintes"], "meta": sortie["meta"]}, indent=1))

    # -- services ----------------------------------------------------------
    def _ligne(self, obj, exclure=("id",)):
        d = {}
        for f in obj._meta.concrete_fields:
            if f.name in exclure or getattr(f, "auto_now", False) or getattr(f, "auto_now_add", False):
                continue
            d[f.attname] = _ser(getattr(obj, f.attname), self.Model, self.QuerySet)
        return d

    def services(self):
        from django.core.management import call_command
        from django.db import transaction

        from argument_manager.models import TrameNarrative
        from case_manager.archive_service import rebuild_global_exhibits
        from case_manager.exhibit_service import rebuild_produced_exhibits, refresh_case_exhibits
        from case_manager.models import ExhibitRegistry, LegalCase, ProducedExhibit
        from document_manager.management.commands import backfill_embeddings as be
        from email_manager.models import Quote as EmailQuote
        from pdf_manager.models import Quote as PDFQuote

        out = {}

        def isole(cle, fn):
            point = transaction.savepoint()
            self.vus = []
            self.actif = True
            try:
                res = fn()
                res["ens_instanciees"] = P.ensemble(f"{l}:{pk}" for l, pk in self.vus if l != "trame")
                out[cle] = res
            except Exception as e:  # noqa: BLE001
                out[cle] = {"erreur": f"{type(e).__name__}: {e}"}
            finally:
                self.actif = False
                transaction.savepoint_rollback(point)

        for pk in LegalCase._base_manager.order_by("pk").values_list("pk", flat=True):
            def pieces(pk=pk):
                refresh_case_exhibits(pk)
                registre = P.ensemble(self._ligne(e) for e in ExhibitRegistry._base_manager.filter(case_id=pk))
                n = rebuild_produced_exhibits(pk)
                produites = P.sequence(self._ligne(p) for p in
                                       ProducedExhibit._base_manager.filter(case_id=pk).order_by("sort_order", "pk"))
                return {"n": n, "ens_registre": registre, "seq_pieces_produites": produites}
            isole(f"cause:{pk}:pieces", pieces)

        archive = LegalCase._base_manager.filter(title="MASTER ARCHIVE - ALL EVIDENCE").order_by("pk").first()
        if archive:
            def globale():
                n = rebuild_global_exhibits(archive.pk)
                return {"n": n, "seq_pieces_produites": P.sequence(
                    self._ligne(p) for p in ProducedExhibit._base_manager.filter(case_id=archive.pk)
                    .order_by("sort_order", "pk"))}
            isole("archive_globale", globale)

        def rattrapage():
            choisies = {}

            def sans_appel(commande, cfg, lignes):
                choisies.setdefault(cfg.label, []).extend(r.pk for r in lignes)

            original = be.Command._embed_and_update
            be.Command._embed_and_update = sans_appel
            try:
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    call_command("backfill_embeddings")
            finally:
                be.Command._embed_and_update = original
            return {f"ens_{k}": P.ensemble(v) for k, v in sorted(choisies.items())}
        isole("rattrapage_plongements", rattrapage)

        for pk in TrameNarrative._base_manager.order_by("pk").values_list("pk", flat=True):
            trame = TrameNarrative._base_manager.get(pk=pk)
            isole(f"trame:{pk}:chronologie", lambda t=trame: {
                "seq_chronologie": _ser(t.get_chronological_evidence(), self.Model, self.QuerySet)})
            isole(f"trame:{pk}:documents_sources", lambda t=trame: {
                "documents_sources": _ser(t.get_source_documents(), self.Model, self.QuerySet)})

        # Les tables, sur leurs colonnes historiques : `regime` n'existe pas avant la
        # migration ; sa valeur est contrôlée à part (instantane_t11.py).
        for cle, modele in (("email_quote", EmailQuote), ("pdf_quote", PDFQuote)):
            out[f"table_{cle}"] = P.ensemble(
                self._ligne(q, exclure=("id", "embedding", "regime"))
                | {"pk": q.pk, "created_at": str(q.created_at), "updated_at": str(q.updated_at),
                   "embedding_nul": q.embedding is None}
                for q in modele._base_manager.order_by("pk"))
            out[f"visibles_{cle}"] = modele._default_manager.count()
        for champ in ("citations_courriel", "citations_pdf"):
            liaison = getattr(TrameNarrative, champ).through
            cols = [f.attname for f in liaison._meta.concrete_fields if f.name != "id"]
            out[f"liaison_{champ}"] = P.ensemble(list(r) for r in liaison.objects.values_list(*cols))
        return out


def _compter(valeurs):
    out = {}
    for v in valeurs:
        out[v] = out.get(v, 0) + 1
    return out


def _ser(valeur, Model, QuerySet, profondeur=0):
    """Sérialisation des résultats de service : les listes restent des séquences,
    les ensembles Python sont triés (ils n'ont pas d'ordre)."""
    if profondeur > 6:
        return "…"
    if valeur is None or isinstance(valeur, (str, int, float, bool)):
        return valeur
    if isinstance(valeur, Model):
        return f"{valeur._meta.label}#{valeur.pk}"
    if isinstance(valeur, QuerySet):
        return [_ser(v, Model, QuerySet, profondeur + 1) for v in valeur]
    if isinstance(valeur, dict):
        return {str(k): _ser(v, Model, QuerySet, profondeur + 1) for k, v in valeur.items()}
    if isinstance(valeur, (list, tuple)):
        return [_ser(v, Model, QuerySet, profondeur + 1) for v in valeur]
    if isinstance(valeur, (set, frozenset)):
        return P.ensemble(_ser(v, Model, QuerySet, profondeur + 1) for v in valeur)
    return str(valeur)


def _texte_docx(octets):
    """Le texte du corps d'un .docx, dans l'ordre (SÉQUENCE). Les métadonnées
    (dates de création du fichier) sont hors projection."""
    import re
    try:
        with zipfile.ZipFile(io.BytesIO(octets)) as z:
            xml = z.read("word/document.xml").decode("utf-8")
    except (zipfile.BadZipFile, KeyError):
        return "illisible:" + P.empreinte(len(octets))
    return P.empreinte(re.sub(r"<[^>]+>", "\n", xml))


if __name__ == "__main__":
    main()
