"""Contre-épreuves B : patch livré intact, deux connexions, données synthétiques."""
import json
import threading
from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType
from django.db import connection, connections
from django.test import RequestFactory

from document_manager import concordance as svc
from document_manager.models import LibraryNode, NoeudArchive, Statement
from document_manager.protection import SuppressionRefusee
from document_manager.test_e01_numerotation import (
    C0ARepriseConcurrence, _citations_synthetiques,
    _dans_une_autre_connexion, ajouter,
)


class ContreEpreuvesB(C0ARepriseConcurrence):
    """Les trois tests A hérités servent de témoins; deux expériences B les complètent."""

    def test_remplacement_a_effectif_constant_doit_refuser_la_suppression(self):
        for type_tardif in ('Statement', 'Quote'):
            with self.subTest(type_tardif=type_tardif):
                parent, e1, e2 = self._bloc()
                observations = {'type_tardif': type_tardif}
                with connection.cursor() as cursor:
                    cursor.execute('SELECT pg_backend_pid()')
                    observations['connexion_T1'] = cursor.fetchone()[0]

                def remplacer():
                    with connection.cursor() as cursor:
                        cursor.execute('SELECT pg_backend_pid()')
                        observations['connexion_T2'] = cursor.fetchone()[0]
                    # Deux opérations ordinaires, validées sur une autre connexion.
                    svc.supprimer_occurrence(LibraryNode.objects.get(pk=e1.pk))
                    p = LibraryNode.objects.get(pk=parent.pk)
                    if type_tardif == 'Quote':
                        contenu, _ = _citations_synthetiques()
                    else:
                        contenu = Statement.objects.create(text='texte enfant intercalé')
                    n = p.add_child(document=self.cible, item='enfant non contrôlé',
                                    content_object=contenu)
                    observations.update(tardif_pk=n.pk, tardif_path=n.path,
                                        contenu_pk=contenu.pk)

                original = svc.archiver_noeud
                premiers = []

                def apres_controle(noeud, **kwargs):
                    if not premiers:
                        premiers.append(True)
                        _dans_une_autre_connexion(remplacer)
                    return original(noeud, **kwargs)

                refus = None
                with patch('document_manager.concordance.archiver_noeud',
                           side_effect=apres_controle):
                    try:
                        resultat = svc.supprimer_occurrence(parent)
                    except SuppressionRefusee as erreur:
                        refus = str(erreur)
                        resultat = None
                observations.update(
                    refus=refus, retour=resultat,
                    tardif_encore_present=LibraryNode.objects.filter(
                        pk=observations['tardif_pk']).exists(),
                    tardif_archive=NoeudArchive.objects.filter(
                        noeud_pk=observations['tardif_pk']).exists(),
                    initialement_controles=[parent.pk, e1.pk, e2.pk],
                )
                print('B_EFFECTIF_CONSTANT ' + json.dumps(observations, ensure_ascii=False),
                      flush=True)
                self.assertIsNotNone(
                    refus, 'UC14 : un enfant hors du bloc archivé a été retiré sans archive')

    def test_reproduire_ajout_en_attente_apres_le_controle_final(self):
        from document_manager.views.produced_views import (
            _get_and_process_tree, ajax_add_node,
        )
        parent = ajouter(self.rc, self.cible, 'tardif', 'parent bientôt retiré')
        observations = {'parent_pk': parent.pk, 'parent_path': parent.path}
        pret = threading.Event()
        erreurs = []
        fils = []

        def ajouter_apres_controle():
            connections.close_all()
            try:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT pg_backend_pid()')
                    observations['connexion_T2'] = cursor.fetchone()[0]

                def avant_update(execute, sql, params, many, context):
                    if (sql.startswith('UPDATE "document_manager_librarynode"')
                            and 'numchild' in sql and parent.path in (params or ())):
                        pret.set()  # L'UPDATE du parent attend sa suppression T1.
                    return execute(sql, params, many, context)

                request = RequestFactory().post('/', {'item': 'enfant tardif',
                                                      'text': 'texte enfant tardif'})
                with connection.execute_wrapper(avant_update):
                    reponse = ajax_add_node(request, parent.pk)
                observations['http_ajout'] = reponse.status_code
                observations['reponse_ajout'] = json.loads(reponse.content)
            except BaseException as erreur:
                erreurs.append(erreur)
            finally:
                connection.close()

        def apres_lecture_finale(execute, sql, params, many, context):
            resultat = execute(sql, params, many, context)
            if (sql.startswith('SELECT') and '"document_manager_librarynode"' in sql
                    and ' LIKE ' in sql and 'LIMIT 1' in sql
                    and parent.path + '%' in (params or ())):
                observations['controle_final_lu_avant_l_ajout'] = True
                fil = threading.Thread(target=ajouter_apres_controle, daemon=True)
                fils.append(fil)
                fil.start()
                if not pret.wait(10):
                    raise RuntimeError('T2 n’a pas atteint l’UPDATE du parent')
            return resultat

        with connection.cursor() as cursor:
            cursor.execute('SELECT pg_backend_pid()')
            observations['connexion_T1'] = cursor.fetchone()[0]
        try:
            with connection.execute_wrapper(apres_lecture_finale):
                observations['retour_suppression'] = svc.supprimer_occurrence(parent)
        finally:
            for fil in fils:
                fil.join(10)
                if fil.is_alive():
                    raise RuntimeError('T2 encore en attente après la fin de T1')
        if erreurs:
            raise erreurs[0]
        pk = observations['reponse_ajout']['new_node']['id']
        enfant = LibraryNode.objects.get(pk=pk)

        def ids_affiches(noeuds):
            return {n.pk for n in noeuds}.union(*[
                ids_affiches(n.children_list) for n in noeuds])

        observations.update(
            parent_existe=LibraryNode.objects.filter(pk=parent.pk).exists(),
            enfant_pk=pk, enfant_path=enfant.path,
            enfant_archive=NoeudArchive.objects.filter(noeud_pk=pk).exists(),
            texte_conserve=enfant.content_object.text,
            enfant_affiche=pk in ids_affiches(_get_and_process_tree(self.cible)),
        )
        print('B_ORPHELIN_APRES_CONTROLE ' + json.dumps(observations, ensure_ascii=False),
              flush=True)
        # Ce succès atteste la reproduction du risque, pas sa conformité fonctionnelle.
        self.assertEqual(observations['http_ajout'], 200)
        self.assertFalse(observations['parent_existe'])
        self.assertFalse(observations['enfant_affiche'])
        self.assertEqual(enfant.path[:-enfant.steplen], parent.path)
