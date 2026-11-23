#!/usr/bin/env node
// Produit le document Word à partir du JSON écrit par assembler.py.
// Usage : node rendre_docx.js demande_assemblee.json demande_assemblee.docx
// Dépendance : le paquet npm « docx » (npm install docx).
//
// Les paragraphes numérotés sont les items d'UNE seule liste Word
// (référence « demande ») : niveau 0 = 1., 2., 3. ; niveau 1 = a), b), c).
// Word gère la numérotation : elle est continue sur toute la demande, à
// travers les intertitres, et les sous-paragraphes recommencent à a) sous
// chaque paragraphe. Les numéros calculés par assembler.py ne servent qu'aux
// renvois rendus en texte.
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, LevelFormat,
  Table, TableRow, TableCell, TableLayoutType, WidthType, ShadingType,
} = require('docx');

const [, , entree, sortie] = process.argv;
if (!entree || !sortie) { console.error('usage : node rendre_docx.js entree.json sortie.docx'); process.exit(1); }
const { elements } = JSON.parse(fs.readFileSync(entree, 'utf8'));
const avecAnnexes = elements.some(e => e.type === 'titre_annexe');

const POLICE = 'Times New Roman';
const RETRAIT = 720;        // 0,5 po
const RETRAIT_SOUS = 1440;  // 1 po
const LARGEUR_LETTRE = 12240;
const MARGE = 1440;
const LARGEUR_UTILE = LARGEUR_LETTRE - 2 * MARGE;
const MARGE_CELLULE = 90;

// Mise en forme en ligne : **gras**, *italique*, `chemin` (rendu sans accents graves).
function runs(texte, style = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  let i = 0, m;
  while ((m = re.exec(texte)) !== null) {
    if (m.index > i) out.push(new TextRun({ ...style, text: texte.slice(i, m.index) }));
    const t = m[0];
    if (t.startsWith('**')) out.push(new TextRun({ ...style, text: t.slice(2, -2), bold: true }));
    else if (t.startsWith('*')) out.push(new TextRun({ ...style, text: t.slice(1, -1), italics: true }));
    else out.push(new TextRun({ ...style, text: t.slice(1, -1) }));
    i = m.index + t.length;
  }
  if (i < texte.length) out.push(new TextRun({ ...style, text: texte.slice(i) }));
  return out;
}

function rendreTableau(lignes) {
  // Réserver la place des libellés courts et répartir l'espace restant
  // selon la longueur moyenne du texte qui devra passer à la ligne.
  const colonnes = lignes[0].map((_, i) => lignes.map(l => l[i].length));
  const minimums = colonnes.map(longueurs => Math.max(1000,
    2 * MARGE_CELLULE + 100 * Math.min(14, Math.max(...longueurs))));
  const tailleMinimale = minimums.reduce((a, b) => a + b, 0);
  const poids = colonnes.map(longueurs => longueurs.reduce((s, l) => s + Math.max(0, l - 14), 0));
  const total = poids.reduce((a, b) => a + b, 0);
  const disponible = Math.max(0, LARGEUR_UTILE - tailleMinimale);
  const facteur = Math.min(1, LARGEUR_UTILE / tailleMinimale);
  const largeurs = minimums.map((minimum, i) => Math.floor(minimum * facteur
    + disponible * (total ? poids[i] / total : 1 / poids.length)));
  largeurs[largeurs.length - 1] += LARGEUR_UTILE - largeurs.reduce((a, b) => a + b, 0);

  const rows = lignes.map((ligne, i) => {
    const entete = i === 0;
    const style = entete ? { font: POLICE, size: 22, bold: true } : { font: POLICE, size: 22 };
    const children = ligne.map((texte, j) => new TableCell({
      width: { size: largeurs[j], type: WidthType.DXA },
      shading: entete ? { type: ShadingType.CLEAR, fill: 'E8E8E8' } : undefined,
      children: [new Paragraph({
        spacing: { before: 0, after: 0, line: 240 },
        children: runs(texte, style),
      })],
    }));
    return new TableRow({ tableHeader: entete, cantSplit: true, children });
  });
  return new Table({
    width: { size: LARGEUR_UTILE, type: WidthType.DXA },
    columnWidths: largeurs,
    layout: TableLayoutType.FIXED,
    margins: { top: MARGE_CELLULE, bottom: MARGE_CELLULE, left: MARGE_CELLULE, right: MARGE_CELLULE },
    rows,
  });
}

const enfants = [];
let precedent = null;
for (const e of elements) {
  switch (e.type) {
    case 'titre':
      enfants.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: runs(e.texte) })); break;
    case 'intertitre':
      enfants.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: runs(e.texte) })); break;
    case 'titre_annexe':
      enfants.push(new Paragraph({ heading: HeadingLevel.HEADING_1,
        pageBreakBefore: true, children: runs(e.texte) })); break;
    case 'section_annexe':
      enfants.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: runs(e.texte) })); break;
    case 'sous_section_annexe':
      enfants.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: runs(e.texte) })); break;
    case 'puce':
      enfants.push(new Paragraph({ numbering: { reference: 'puces-annexes', level: e.niveau },
        spacing: { after: 80, line: 264 },
        children: runs(e.texte) })); break;
    case 'tableau':
      enfants.push(rendreTableau(e.cellules)); break;
    case 'para':
      enfants.push(new Paragraph({ numbering: { reference: 'demande', level: 0 },
        alignment: AlignmentType.JUSTIFIED, children: runs(e.texte) })); break;
    case 'sous':
      enfants.push(new Paragraph({ numbering: { reference: 'demande', level: 1 },
        alignment: AlignmentType.JUSTIFIED, children: runs(e.texte) })); break;
    case 'suite':
      enfants.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED,
        indent: { left: precedent === 'sous' ? RETRAIT_SOUS : RETRAIT }, children: runs(e.texte) })); break;
    case 'citation':
      enfants.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED,
        indent: { left: RETRAIT_SOUS, right: RETRAIT }, children: runs(e.texte) })); break;
    default:
      enfants.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED,
        spacing: precedent === 'tableau' ? { before: 120 } : undefined, children: runs(e.texte) }));
  }
  if (e.type !== 'suite') precedent = e.type;
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: POLICE, size: 24 }, paragraph: { spacing: { after: 160, line: 276 } } } },
    paragraphStyles: [
      ...(avecAnnexes ? [{ id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: POLICE, size: 32, bold: true },
        paragraph: { spacing: { after: 240 }, keepNext: true, outlineLevel: 0 } }] : []),
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: POLICE, size: 28, bold: true },
        paragraph: { spacing: { before: 360, after: 200 }, keepNext: true, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: POLICE, size: 24, bold: true, italics: true },
        paragraph: { spacing: { before: 240, after: 120 }, keepNext: true, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [{
      reference: 'demande',
      levels: [
        { level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: RETRAIT, hanging: RETRAIT } } } },
        { level: 1, format: LevelFormat.LOWER_LETTER, text: '%2)', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: RETRAIT_SOUS, hanging: 504 } } } },
      ],
    }, ...(avecAnnexes ? [{
      reference: 'puces-annexes',
      levels: Array.from({ length: 9 }, (_, level) => ({
        level, format: LevelFormat.BULLET, text: '\u2022', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 360 * (level + 1), hanging: 270 } } },
      })),
    }] : [])],
  },
  sections: [{
    properties: { page: { size: { width: LARGEUR_LETTRE, height: 15840 },
      margin: { top: MARGE, right: MARGE, bottom: MARGE, left: MARGE } } },
    children: enfants,
  }],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(sortie, buf); });
