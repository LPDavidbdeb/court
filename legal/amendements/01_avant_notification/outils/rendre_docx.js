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
} = require('docx');

const [, , entree, sortie] = process.argv;
if (!entree || !sortie) { console.error('usage : node rendre_docx.js entree.json sortie.docx'); process.exit(1); }
const { elements } = JSON.parse(fs.readFileSync(entree, 'utf8'));

const POLICE = 'Times New Roman';
const RETRAIT = 720;        // 0,5 po
const RETRAIT_SOUS = 1440;  // 1 po

// Mise en forme en ligne : **gras**, *italique*, `chemin` (rendu sans accents graves).
function runs(texte) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  let i = 0, m;
  while ((m = re.exec(texte)) !== null) {
    if (m.index > i) out.push(new TextRun(texte.slice(i, m.index)));
    const t = m[0];
    if (t.startsWith('**')) out.push(new TextRun({ text: t.slice(2, -2), bold: true }));
    else if (t.startsWith('*')) out.push(new TextRun({ text: t.slice(1, -1), italics: true }));
    else out.push(new TextRun(t.slice(1, -1)));
    i = m.index + t.length;
  }
  if (i < texte.length) out.push(new TextRun(texte.slice(i)));
  return out;
}

const enfants = [];
let precedent = null;
for (const e of elements) {
  switch (e.type) {
    case 'titre':
      enfants.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: runs(e.texte) })); break;
    case 'intertitre':
      enfants.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: runs(e.texte) })); break;
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
      enfants.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, children: runs(e.texte) }));
  }
  if (e.type !== 'suite') precedent = e.type;
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: POLICE, size: 24 }, paragraph: { spacing: { after: 160, line: 276 } } } },
    paragraphStyles: [
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
    }],
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children: enfants,
  }],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(sortie, buf); });
