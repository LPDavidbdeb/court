#!/usr/bin/env python3
"""Assemble les blocs de la demande amendée et produit un document Word.

Usage :
    python3 assembler.py                 # lit ../blocs/ordre.txt, écrit dans ../build/
    python3 assembler.py --sans-word     # contrôles et Markdown assemblé seulement
    python3 assembler.py --ordre autre.txt --sortie /tmp/essai

Étapes (voir blocs/METHODE.md, § 6) :
1. lit le fichier d'ordre et les blocs, dans cet ordre ;
2. retire l'en-tête YAML et tout ce qui suit `<!-- fin-du-texte -->` ;
3. numérote : paragraphes `1. ` (liste continue sur toute la demande),
   sous-paragraphes `   a) ` (lettrés, recommencent à chaque paragraphe) ;
4. contrôle les étiquettes `{#…}` (uniques) et les renvois `{§…}` (résolus) ;
   signale les numéros de paragraphe écrits en dur ; erreur bloquante sinon ;
5. relance la vérification des citations (`verif_citations.py`) ;
6. écrit `demande_assemblee.md` (numéros calculés, pour relecture) et
   `demande_assemblee.json`, puis appelle `rendre_docx.js`, qui produit
   `demande_assemblee.docx` : les paragraphes y sont les items d'UNE liste Word ;
   la numérotation est gérée par Word.

Renvois rendus en texte : `{§etiq}` -> « § N » ; `{§etiq/b}` -> « § N b) » ;
`{§etiq1..etiq2}` -> « §§ N à M ». Le .md reste la source : réassembler après
chaque modification.
"""
import argparse, json, pathlib, re, subprocess, sys

ICI = pathlib.Path(__file__).resolve().parent
BLOCS = ICI.parent / 'blocs'
MARQUEUR = '<!-- fin-du-texte -->'
RE_ETIQ = re.compile(r'\s*\{#([a-z0-9][a-z0-9-]*)\}\s*$')
RE_RENVOI = re.compile(r'\{§([a-z0-9][a-z0-9-]*)(?:\.\.([a-z0-9][a-z0-9-]*))?(?:/([a-z]))?\}')
RE_DUR = re.compile(r'(?<![«\w])§§?\s?\d+|\*\*\d+\.\*\*')
LETTRES = 'abcdefghijklmnopqrstuvwxyz'


class Erreur(Exception):
    pass


def lire_bloc(chemin):
    texte = chemin.read_text(encoding='utf-8')
    meta = {}
    if texte.startswith('---\n'):
        fin = texte.index('\n---\n', 4)
        for ligne in texte[4:fin].splitlines():
            if ':' in ligne and not ligne.lstrip().startswith('#'):
                k, v = ligne.split(':', 1)
                meta[k.strip()] = v.split(' #')[0].strip()
        texte = texte[fin + 5:]
    if MARQUEUR not in texte:
        raise Erreur(f'{chemin.name} : marqueur {MARQUEUR} absent')
    return meta, texte.split(MARQUEUR)[0]


def analyser(nom, corps):
    """Découpe le corps d'un bloc en éléments."""
    elems, courant = [], None
    for brute in corps.splitlines():
        ligne = brute.rstrip()
        if not ligne.strip():
            courant = None
            continue
        if ligne.strip() == '---':
            courant = None
            continue
        if ligne.startswith('#### '):
            elems.append({'type': 'intertitre', 'texte': ligne[5:].strip()}); courant = None; continue
        if ligne.startswith('# '):
            elems.append({'type': 'titre', 'texte': ligne[2:].strip()}); courant = None; continue
        if ligne.startswith('#'):
            raise Erreur(f'{nom} : niveau de titre non prévu : {ligne[:40]}')
        m = re.match(r'^1\.\s+(.*)$', ligne)
        if m:
            courant = {'type': 'para', 'texte': m.group(1)}; elems.append(courant); continue
        if re.match(r'^\d+\.\s', ligne):
            raise Erreur(f'{nom} : paragraphe numéroté autrement que « 1. » : {ligne[:40]}')
        m = re.match(r'^ {2,4}([a-z])\)\s+(.*)$', ligne)
        if m:
            courant = {'type': 'sous', 'texte': m.group(2)}; elems.append(courant); continue
        if ligne.startswith('>'):
            courant = {'type': 'citation', 'texte': ligne.lstrip('> ').strip()}; elems.append(courant); continue
        if courant is not None:
            courant['texte'] += ' ' + ligne.strip()
            continue
        retrait = ligne.startswith('   ')
        courant = {'type': 'suite' if retrait else 'texte', 'texte': ligne.strip()}
        elems.append(courant)
    return elems


def assembler(ordre, sortie, avec_word=True):
    noms = [l.strip() for l in ordre.read_text(encoding='utf-8').splitlines()
            if l.strip() and not l.startswith('#')]
    tous, alertes = [], []
    for nom in noms:
        meta, corps = lire_bloc(BLOCS / nom)
        for e in analyser(nom, corps):
            e['bloc'] = nom
            tous.append(e)

    # Numérotation et étiquettes
    etiquettes, n, lettre = {}, 0, 0
    for e in tous:
        if e['type'] == 'para':
            n += 1; lettre = 0; e['num'] = n; e['ref'] = f'{n}'
        elif e['type'] == 'sous':
            if n == 0:
                raise Erreur(f"{e['bloc']} : sous-paragraphe avant tout paragraphe")
            e['num'] = LETTRES[lettre]; lettre += 1; e['ref'] = f"{n} {e['num']})"; e['parent'] = n
        m = RE_ETIQ.search(e['texte'])
        if m:
            if e['type'] not in ('para', 'sous'):
                raise Erreur(f"{e['bloc']} : étiquette {m.group(1)} hors d'un paragraphe numéroté")
            if m.group(1) in etiquettes:
                raise Erreur(f"étiquette en double : {m.group(1)}")
            etiquettes[m.group(1)] = e
            e['texte'] = RE_ETIQ.sub('', e['texte'])
        if '{#' in e['texte']:
            raise Erreur(f"{e['bloc']} : étiquette mal placée (doit finir le paragraphe) : {e['texte'][:60]}")

    # Renvois
    def num(etiq):
        if etiq not in etiquettes:
            raise Erreur(f'renvoi orphelin : {etiq}')
        return etiquettes[etiq]

    def rendre(m):
        a, b, sous = m.group(1), m.group(2), m.group(3)
        ea = num(a)
        if b:
            eb = num(b)
            return f"§§ {ea['ref']} à {eb['ref']}"
        if sous:
            if ea['type'] != 'para':
                raise Erreur(f'renvoi {a}/{sous} : {a} n’est pas un paragraphe')
            return f"§ {ea['ref']} {sous})"
        return f"§ {ea['ref']}"

    for e in tous:
        brut = RE_RENVOI.sub('', e['texte'])
        for dur in RE_DUR.findall(brut):
            alertes.append(f"{e['bloc']} : numéro écrit en dur « {dur} » dans : {e['texte'][:70]}")
        e['texte'] = RE_RENVOI.sub(rendre, e['texte'])
        # « ({§x/a}) » donnerait « (§ 3 a)) » : une seule parenthèse fermante.
        e['texte'] = re.sub(r'(§ \d+ [a-z]\))\)', r'\1', e['texte'])
        if '{§' in e['texte']:
            raise Erreur(f"{e['bloc']} : renvoi mal formé : {e['texte'][:70]}")

    # Markdown assemblé (relecture)
    sortie.mkdir(parents=True, exist_ok=True)
    lignes = []
    for e in tous:
        t = e['type']
        if t == 'titre': lignes += ['', f"# {e['texte']}", '']
        elif t == 'intertitre': lignes += ['', f"#### {e['texte']}", '']
        elif t == 'para': lignes += ['', f"**{e['num']}.** {e['texte']}"]
        elif t == 'sous': lignes += [f"  {e['num']}) {e['texte']}"]
        elif t == 'suite': lignes += ['', f"  {e['texte']}"]
        elif t == 'citation': lignes += ['', f"> {e['texte']}"]
        else: lignes += ['', e['texte']]
    (sortie / 'demande_assemblee.md').write_text('\n'.join(lignes).strip() + '\n', encoding='utf-8')
    (sortie / 'demande_assemblee.json').write_text(
        json.dumps({'elements': tous}, ensure_ascii=False, indent=1), encoding='utf-8')

    # Citations
    verif = subprocess.run([sys.executable, str(ICI / 'verif_citations.py')] + [str(BLOCS / x) for x in noms],
                           capture_output=True, text=True)
    non = [l for l in verif.stdout.splitlines() if l.startswith('NO')]

    if avec_word:
        r = subprocess.run(['node', str(ICI / 'rendre_docx.js'), str(sortie / 'demande_assemblee.json'),
                            str(sortie / 'demande_assemblee.docx')], capture_output=True, text=True)
        if r.returncode:
            raise Erreur('rendre_docx.js : ' + (r.stderr or r.stdout))

    print(f'{len(noms)} bloc(s), {n} paragraphe(s) numéroté(s), {len(etiquettes)} étiquette(s).')
    for a in alertes:
        print('ALERTE ' + a)
    for l in non:
        print('CITATION ' + l)
    print(f'Sortie : {sortie}')
    return 0


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--ordre', default=str(BLOCS / 'ordre.txt'))
    p.add_argument('--sortie', default=str(ICI.parent / 'build'))
    p.add_argument('--sans-word', action='store_true')
    a = p.parse_args()
    try:
        sys.exit(assembler(pathlib.Path(a.ordre), pathlib.Path(a.sortie), not a.sans_word))
    except Erreur as ex:
        print('ERREUR ' + str(ex))
        sys.exit(2)
