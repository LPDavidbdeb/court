import copy

from legal.verification_appuis.commun import Refus, empreinte, octets_json
from legal.verification_appuis.constat import capturer
from legal.verification_appuis.journal import proposer
from legal.verification_appuis.observations import lire_observations
from legal.verification_appuis.serie_1 import verifier_serie, enregistrer_serie, tableau_ecarts
from legal.verification_appuis.tests.aide import CasVA
from legal.verification_appuis.tests.test_va04 import observation


class Serie1(CasVA):
    def preparation(self):
        c=capturer(self.source,self.concordance)
        c['liens']=[{'id':i,'statement_id':1,'entree_id':1,'cote_citee':'P-1','via_liasse':False} for i in range(99,142)]
        w={'liens':[{'lien_id':99,'priorite':0}]+[{'lien_id':i,'priorite':1} for i in range(100,142)]}
        p=self.repertoire/'piece_fictive.txt';p.write_text('FICTIF — déclaration de test')
        ps=[]
        for i in range(100,140):
            o=observation();o.update(id=f'FICTIF-S1-{i}',liens=[i],grille_version='1.1',ecarts=[],
                                    empreinte_enonce=c['enonces'][0]['empreinte_texte'],supports=[{'chemin':str(p),'sha256':empreinte(p.read_bytes())}])
            ps.append(o)
        a=self.repertoire/'accord_fictif.json'
        a.write_bytes(octets_json({'schema':'va-accords/1','stories':{'VA06':{'auteur':'LP','mode':'LECTURE_SEULE','reference_message':'LP FICTIF — aucun accès réel'}}}))
        return c,w,ps,a

    def test_ordre_exact_quarante_et_aucune_decision_lp(self):
        c,w,ps,a=self.preparation()
        self.assertEqual(verifier_serie(c,w,ps),list(range(100,140)))
        for erreur in (ps[:-1],list(reversed(ps)),ps+[copy.deepcopy(ps[-1])]):
            with self.assertRaisesRegex(Refus,'Périmètre'):
                verifier_serie(c,w,erreur)
        ps[0].update(auteur='LP',avancement='VALIDE',decision_reference='LP FICTIF')
        with self.assertRaisesRegex(Refus,'propositions CODEX'):
            verifier_serie(c,w,ps)

    def test_support_final_change_arrete_avant_tout_ajout(self):
        c,w,ps,a=self.preparation()
        p=self.repertoire/'derniere_piece_fictive.txt';p.write_text('FICTIF avant')
        ps[-1]['supports']=[{'chemin':str(p),'sha256':empreinte(p.read_bytes())}]
        j=self.repertoire/'journal_fictif.jsonl';j.write_bytes(b'')
        p.write_text('FICTIF après')
        with self.assertRaisesRegex(Refus,'Support'):
            enregistrer_serie(a,c,w,ps,j)
        self.assertEqual(j.read_bytes(),b'')
        p.write_text('FICTIF avant')
        self.assertEqual(enregistrer_serie(a,c,w,ps,j),(40,2))
        self.assertEqual({o['avancement'] for o in lire_observations(j)},{'PROPOSE'})

    def test_tableau_place_les_contradictions_en_premier(self):
        c,w,ps,a=self.preparation()
        for o,degre in zip(ps,('NE_L_ETABLIT_PAS','CONTREDIT','ETABLIT_EN_CADRANT_AUTREMENT')):
            o['ecarts']=[{'type':'SENS','degre':degre,'description':'Écart FICTIF'}]
        self.assertEqual([e['lien'] for e in tableau_ecarts(ps)],[101,102,100])
