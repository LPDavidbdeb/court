#!/usr/bin/env python3
"""Assemble les blocs et les annexes de la demande amendée, en Markdown et Word.

Usage :
    python3 assembler.py                 # lit ../blocs/ordre.txt, écrit dans ../build/
    python3 assembler.py --sans-word     # contrôles et Markdown assemblé seulement
    python3 assembler.py --sans-annexes  # sortie limitée aux blocs
    python3 assembler.py --ordre autre.txt --sortie /tmp/essai

Étapes (voir blocs/METHODE.md, § 6) :
1. lit le fichier d'ordre (blocs et titres de partie introduits par `## `) ;
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
`{annexe:identifiant}` -> « l'annexe N », selon blocs/annexes/ordre_annexes.txt.
"""
import argparse, json, pathlib, re, subprocess, sys

ICI = pathlib.Path(__file__).resolve().parent
BLOCS = ICI.parent / 'blocs'
ANNEXES = BLOCS / 'annexes'
MARQUEUR = '<!-- fin-du-texte -->'
RE_ETIQ = re.compile(r'\s*\{#([a-z0-9][a-z0-9-]*)\}\s*$')
RE_ETIQ_ANNEXE = re.compile(r'\s*\{#([a-zA-Z0-9][a-zA-Z0-9-]*)\}\s*$')
RE_RENVOI = re.compile(r'\{§([a-z0-9][a-z0-9-]*)(?:\.\.([a-z0-9][a-z0-9-]*))?(?:/([a-z]))?\}')
ID_ANNEXE = r'[a-zA-Z0-9][a-zA-Z0-9_-]*'
RE_ANNEXE = re.compile(r'\{annexe:(' + ID_ANNEXE + r')\}')
RE_DUR = re.compile(r'(?<![«\w])§§?\s?\d+|\*\*\d+\.\*\*')
LETTRES = 'abcdefghijklmnopqrstuvwxyz'


class Erreur(Exception):
    pass


def lire_bloc(chemin):
    texte = chemin.read_text(encoding='utf-8')
    meta = {}
    if texte.startswith('---\n'):
        fin = texte.find('\n---\n', 4)
        if fin == -1:
            raise Erreur(f'{chemin.name} : en-tête non fermé')
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


def lire_ordre(chemin, *, titres_partie=False):
    entrees = []
    for ligne in chemin.read_text(encoding='utf-8').splitlines():
        if titres_partie and ligne.startswith('## '):
            titre = ligne[3:].strip()
            if not titre:
                raise Erreur(f'{chemin.name} : titre de partie vide')
            entrees.append(('titre_partie', titre))
        elif ligne.strip() and not ligne.startswith('#'):
            entrees.append(('fichier', ligne.strip()))
    return entrees


def analyser_annexe(nom, corps, numero):
    titre, _, corps = corps.strip().partition('\n')
    if not titre.startswith('# ') or not titre[2:].strip():
        raise Erreur(f'{nom} : titre de l’annexe absent')
    elems = [{'type': 'titre_annexe', 'texte': f'Annexe {numero} — {titre[2:].strip()}'}]
    courant = None
    for ligne in corps.splitlines():
        ligne = ligne.rstrip()
        if not ligne.strip():
            courant = None
            continue
        if ligne.startswith('|'):
            if courant is None or courant['type'] != 'tableau':
                courant = {'type': 'tableau', 'lignes': []}
                elems.append(courant)
            courant['lignes'].append(ligne)
            continue
        titre = re.fullmatch(r'(##|###) (.+)', ligne)
        puce = re.fullmatch(r'( {0,16})- (.+)', ligne)
        if titre:
            type_titre = 'section_annexe' if titre[1] == '##' else 'sous_section_annexe'
            courant = {'type': type_titre, 'texte': titre[2]}
        elif puce:
            courant = {'type': 'puce', 'niveau': len(puce[1]) // 2, 'texte': puce[2]}
        elif courant is not None and courant['type'] in ('texte', 'puce'):
            courant['texte'] += ' ' + ligne.strip()
            continue
        else:
            courant = {'type': 'texte', 'texte': ligne.strip()}
        elems.append(courant)
    for e in elems:
        e['bloc'] = nom
        if e['type'] != 'tableau':
            continue
        lignes = e['lignes']
        cellules = [
            [c.strip().replace(r'\|', '|') for c in re.split(r'(?<!\\)\|', ligne[1:-1])]
            for ligne in lignes
        ]
        if (len(cellules) < 2 or any(not ligne.endswith('|') for ligne in lignes)
                or any(len(rang) != len(cellules[0]) for rang in cellules)
                or not all(re.fullmatch(r':?-{3,}:?', c) for c in cellules[1])):
            raise Erreur(f'{nom} : tableau Markdown mal formé : {lignes[0]}')
        e['cellules'] = cellules[:1] + cellules[2:]
    return elems


def assembler(ordre, sortie, avec_word=True, avec_annexes=True):
    noms, tous, alertes = [], [], []
    for type_entree, valeur in lire_ordre(ordre, titres_partie=True):
        if type_entree == 'titre_partie':
            tous.append({'type': 'titre_partie', 'texte': valeur, 'bloc': ordre.name})
            continue
        nom = valeur
        noms.append(nom)
        _, corps = lire_bloc(BLOCS / nom)
        elements = analyser(nom, corps)
        if (tous and tous[-1]['type'] == 'titre_partie' and elements
                and elements[0]['type'] == 'titre' and elements[0]['texte'] == tous[-1]['texte']):
            # Le bloc reste autonome, mais son titre identique à celui de la partie ne s'affiche qu'une fois.
            elements = elements[1:]
        for e in elements:
            e['bloc'] = nom
            tous.append(e)

    ordre_annexes = ANNEXES / 'ordre_annexes.txt'
    annexes = lire_ordre(ordre_annexes) if ordre_annexes.exists() else []
    numeros_annexes, elements_annexes = {}, []
    for numero, (_, nom) in enumerate(annexes, 1):
        chemin = ANNEXES / nom
        if not chemin.is_file():
            raise Erreur(f'annexe introuvable : {nom}')
        meta, corps = lire_bloc(chemin)
        identifiant = meta.get('annexe', '')
        if not re.fullmatch(ID_ANNEXE, identifiant):
            raise Erreur(f'{nom} : identifiant d’annexe absent ou mal formé')
        if identifiant in numeros_annexes:
            raise Erreur(f'identifiant d’annexe en double : {identifiant}')
        numeros_annexes[identifiant] = numero
        if avec_annexes:
            elements_annexes.extend(analyser_annexe(nom, corps, numero))

    # Numérotation et étiquettes
    etiquettes, n, lettre = {}, 0, 0
    for e in tous + elements_annexes:
        if e['type'] == 'tableau':
            if any('{#' in ligne for ligne in e['lignes']):
                raise Erreur(f"{e['bloc']} : étiquette hors d’un titre de section d’annexe")
            continue
        if e['type'] == 'para':
            n += 1; lettre = 0; e['num'] = n; e['ref'] = f'{n}'
        elif e['type'] == 'sous':
            if n == 0:
                raise Erreur(f"{e['bloc']} : sous-paragraphe avant tout paragraphe")
            e['num'] = LETTRES[lettre]; lettre += 1; e['ref'] = f"{n} {e['num']})"; e['parent'] = n
        re_etiq = RE_ETIQ_ANNEXE if e['type'] == 'section_annexe' else RE_ETIQ
        m = re_etiq.search(e['texte'])
        if m:
            if e['type'] not in ('para', 'sous', 'section_annexe'):
                raise Erreur(f"{e['bloc']} : étiquette {m.group(1)} hors d'un paragraphe numéroté")
            if m.group(1) in etiquettes:
                raise Erreur(f"étiquette en double : {m.group(1)}")
            etiquettes[m.group(1)] = e
            e['texte'] = re_etiq.sub('', e['texte'])
        if '{#' in e['texte']:
            raise Erreur(f"{e['bloc']} : étiquette mal placée : {e['texte'][:60]}")

    # Renvois
    def num(etiq):
        if etiq not in etiquettes or 'ref' not in etiquettes[etiq]:
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

    def rendre_renvoi_annexe(m):
        identifiant = m[1]
        if identifiant not in numeros_annexes:
            raise Erreur(f'renvoi vers une annexe inconnue : {identifiant}')
        return f"l'annexe {numeros_annexes[identifiant]}"

    for e in tous:
        brut = RE_RENVOI.sub('', e['texte'])
        for dur in RE_DUR.findall(brut):
            alertes.append(f"{e['bloc']} : numéro écrit en dur « {dur} » dans : {e['texte'][:70]}")
        e['texte'] = RE_RENVOI.sub(rendre, e['texte'])
        # « ({§x/a}) » donnerait « (§ 3 a)) » : une seule parenthèse fermante.
        e['texte'] = re.sub(r'(§ \d+ [a-z]\))\)', r'\1', e['texte'])
        if '{§' in e['texte']:
            raise Erreur(f"{e['bloc']} : renvoi mal formé : {e['texte'][:70]}")
        e['texte'] = RE_ANNEXE.sub(rendre_renvoi_annexe, e['texte'])
        if '{annexe:' in e['texte']:
            raise Erreur(f"{e['bloc']} : renvoi d’annexe mal formé : {e['texte'][:70]}")

    # Markdown assemblé (relecture)
    sortie.mkdir(parents=True, exist_ok=True)
    lignes = []
    niveau_bloc = '##' if any(e['type'] == 'titre_partie' for e in tous) else '#'
    for e in tous:
        t = e['type']
        if t == 'titre_partie': lignes += ['', f"# {e['texte']}", '']
        elif t == 'titre': lignes += ['', f"{niveau_bloc} {e['texte']}", '']
        elif t == 'intertitre': lignes += ['', f"#### {e['texte']}", '']
        elif t == 'para': lignes += ['', f"**{e['num']}.** {e['texte']}"]
        elif t == 'sous': lignes += [f"  {e['num']}) {e['texte']}"]
        elif t == 'suite': lignes += ['', f"  {e['texte']}"]
        elif t == 'citation': lignes += ['', f"> {e['texte']}"]
        else: lignes += ['', e['texte']]
    markdown = '\n'.join(lignes).strip() + '\n'
    lignes_annexes = []
    for e in elements_annexes:
        t = e['type']
        if t == 'titre_annexe':
            lignes_annexes += ['', f"# {e['texte']}", '']
        elif t == 'section_annexe':
            lignes_annexes += ['', f"## {e['texte']}", '']
        elif t == 'sous_section_annexe':
            lignes_annexes += ['', f"### {e['texte']}", '']
        elif t == 'tableau':
            lignes_annexes += ['', *e['lignes'], '']
        elif t == 'puce':
            retrait = '  ' * e['niveau']
            lignes_annexes.append(f"{retrait}- {e['texte']}")
        else:
            lignes_annexes += ['', e['texte']]
    if lignes_annexes:
        markdown += '\n'.join(lignes_annexes).strip() + '\n'
    (sortie / 'demande_assemblee.md').write_text(markdown, encoding='utf-8')
    (sortie / 'demande_assemblee.json').write_text(
        json.dumps({'elements': tous + elements_annexes}, ensure_ascii=False, indent=1), encoding='utf-8')

    # Citations
    chemins = [BLOCS / nom for nom in noms]
    if avec_annexes:
        chemins.extend(ANNEXES / nom for _, nom in annexes)
    verif = subprocess.run([sys.executable, str(ICI / 'verif_citations.py'), *map(str, chemins)],
                           capture_output=True, text=True)
    non = [l for l in verif.stdout.splitlines() if l.startswith('NO')]

    if avec_word:
        r = subprocess.run(['node', str(ICI / 'rendre_docx.js'), str(sortie / 'demande_assemblee.json'),
                            str(sortie / 'demande_assemblee.docx')], capture_output=True, text=True)
        if r.returncode:
            raise Erreur('rendre_docx.js : ' + (r.stderr or r.stdout))

    nb_etiquettes_annexes = sum(e['type'] == 'section_annexe' for e in etiquettes.values())
    print(f'{len(noms)} bloc(s), {n} paragraphe(s) numéroté(s), '
          f'{len(etiquettes) - nb_etiquettes_annexes} étiquette(s).')
    if elements_annexes:
        print(f'{len(annexes)} annexe(s), {nb_etiquettes_annexes} étiquette(s) d’annexe.')
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
    p.add_argument('--sans-annexes', action='store_true')
    a = p.parse_args()
    try:
        sys.exit(assembler(pathlib.Path(a.ordre), pathlib.Path(a.sortie), not a.sans_word, not a.sans_annexes))
    except Erreur as ex:
        print('ERREUR ' + str(ex))
        sys.exit(2)
