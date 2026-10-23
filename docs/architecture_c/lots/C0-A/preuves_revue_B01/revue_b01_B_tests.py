"""Contre-épreuves B01 indépendantes; données synthétiques, deux connexions réelles."""
import json
from unittest.mock import patch
from django.contrib.contenttypes.models import ContentType
from django.db import connection, connections
from django.test import TransactionTestCase, RequestFactory
from document_manager import concordance as svc
from document_manager.models import LibraryNode, NoeudArchive, Statement, ExtremiteCorrespondance
from document_manager.protection import SuppressionRefusee
from document_manager.test_e01_numerotation import C0ARepriseConcurrence, _citations_synthetiques


def autre_connexion(fonction):
    """T2 validée avant de rendre la main à T1; bornes évitant une attente infinie."""
    import threading
    erreurs=[]
    def cible():
        connections.close_all()
        try:
            with connection.cursor() as c:
                c.execute("SET lock_timeout='3000ms'")
                c.execute("SET statement_timeout='6000ms'")
            fonction()
        except BaseException as e:erreurs.append(e)
        finally:connections.close_all()
    fil=threading.Thread(target=cible,daemon=True);fil.start();fil.join(10)
    if fil.is_alive():raise RuntimeError('T2 encore active; essai non concluant')
    if erreurs:raise erreurs[0]


class RevueB01(TransactionTestCase):
    setUp = C0ARepriseConcurrence.setUp
    _bloc = C0ARepriseConcurrence._bloc

    def _pid(self):
        with connection.cursor() as c:
            c.execute('SELECT pg_backend_pid()');return c.fetchone()[0]

    def _lien(self,noeud):
        corr=svc.relier(self.source,self.cible,[self.ns],[noeud])
        return ExtremiteCorrespondance.objects.get(correspondance=corr,noeud=noeud)

    def _remplacement(self,citation):
        parent,e1,e2=self._bloc();ext=self._lien(e2)
        obs={'experience':'B01_avant_archives','type':'citation' if citation else 'Statement','T1':self._pid()}
        def remplacer():
            obs['T2']=self._pid()
            svc.supprimer_occurrence(LibraryNode.objects.get(pk=e1.pk),motif='retrait T2')
            contenu=_citations_synthetiques()[0] if citation else Statement.objects.create(text='nouveau T2')
            n=LibraryNode.objects.get(pk=parent.pk).add_child(document=self.cible,item='nouveau enfant',content_object=contenu)
            obs.update(e3=n.pk,contenu=contenu.pk)
        original=svc.archiver_noeud;unefois=[]
        def archive(n,**kwargs):
            if not unefois:
                unefois.append(True);autre_connexion(remplacer)
            return original(n,**kwargs)
        refus=None
        with patch('document_manager.concordance.archiver_noeud',side_effect=archive):
            try:svc.supprimer_occurrence(parent)
            except SuppressionRefusee as e:refus=str(e)
        ext.refresh_from_db()
        obs.update(refus=refus,restants=list(LibraryNode.objects.filter(pk__in=[parent.pk,e1.pk,e2.pk,obs['e3']]).values_list('pk',flat=True)),archives=list(NoeudArchive.objects.values_list('noeud_pk','motif')),extremite=(ext.noeud_id,ext.archive_id))
        print('B01_OBSERVATION '+json.dumps(obs,ensure_ascii=False),flush=True)
        self.assertNotEqual(obs['T1'],obs['T2'])
        self.assertIsNotNone(refus,'Remplacement à effectif constant accepté')
        self.assertEqual(set(obs['restants']),{parent.pk,e2.pk,obs['e3']})
        self.assertEqual(obs['archives'],[(e1.pk,'retrait T2')])
        self.assertEqual((ext.noeud_id,ext.archive_id),(e2.pk,None))
        self.assertEqual(LibraryNode.objects.get(pk=parent.pk).numchild,2)

    def test_B01_statement_initial_refuse(self):self._remplacement(False)
    def test_B01_citation_initial_refuse(self):self._remplacement(True)

    def _modification(self,phase,citation):
        from document_manager.views.produced_views import ajax_edit_node
        from email_manager.models import Quote
        parent,e1,e2=self._bloc();ancien=e2.object_id;ext=self._lien(e2)
        obs={'experience':'modification_'+phase,'type':'citation' if citation else 'edition_HTTP','T1':self._pid(),'noeud':e2.pk,'ancien_statement':ancien}
        def modifier():
            obs['T2']=self._pid()
            if citation:
                q=_citations_synthetiques()[0]
                n=LibraryNode.objects.get(pk=e2.pk)
                n.content_type=ContentType.objects.get_for_model(Quote);n.object_id=q.pk;n.save()
                obs['nouveau_contenu']=q.pk
            else:
                request=RequestFactory().post('/',{'item':e2.item,'text':'texte décidé dans T2'})
                reponse=ajax_edit_node(request,e2.pk)
                obs.update(http=reponse.status_code,reponse=json.loads(reponse.content))
                if reponse.status_code!=200 or obs['reponse'].get('status')!='success':
                    raise RuntimeError('T2 n’a pas validé son édition : '+str(obs))
                obs['nouveau_contenu']=LibraryNode.objects.get(pk=e2.pk).object_id
        unefois=[]
        def sql(execute,query,params,many,context):
            if query.startswith('DELETE FROM "document_manager_librarynode"') and e2.pk in (params or ()) and not unefois:
                unefois.append(True);obs['point_intercalage']='avant DELETE SQL, après pre_delete';autre_connexion(modifier)
            return execute(query,params,many,context)
        original=svc.archiver_noeud
        def archive(n,**kwargs):
            if not unefois:
                unefois.append(True);autre_connexion(modifier)
            return original(n,**kwargs)
        refus=None
        try:
            if phase=='avant_archives':
                with patch('document_manager.concordance.archiver_noeud',side_effect=archive):svc.supprimer_occurrence(parent)
            else:
                with connection.execute_wrapper(sql):svc.supprimer_occurrence(parent)
        except SuppressionRefusee as e:refus=str(e)
        ext.refresh_from_db()
        obs.update(refus=refus,restants=list(LibraryNode.objects.filter(pk__in=[parent.pk,e1.pk,e2.pk]).values_list('pk',flat=True)),archives=list(NoeudArchive.objects.values('noeud_pk','statement_pk','texte')),extremite=(ext.noeud_id,ext.archive_id))
        print('B01_OBSERVATION '+json.dumps(obs,ensure_ascii=False),flush=True)
        self.assertTrue(unefois,'Entrelacement non atteint')
        self.assertNotEqual(obs['T1'],obs['T2'])
        self.assertIsNotNone(refus,'UC14 : le contenu de l’occurrence supprimée diffère de celui archivé')
        self.assertEqual(set(obs['restants']),{parent.pk,e1.pk,e2.pk})
        self.assertFalse(NoeudArchive.objects.exists())
        self.assertEqual((ext.noeud_id,ext.archive_id),(e2.pk,None))
        self.assertEqual(LibraryNode.objects.get(pk=e2.pk).object_id,obs['nouveau_contenu'])

    def test_edition_HTTP_avant_archives_refuse_et_annule_tout(self):self._modification('avant_archives',False)
    def test_repointage_citation_avant_archives_refuse_et_annule_tout(self):self._modification('avant_archives',True)
    def test_edition_HTTP_apres_gardes_avant_DELETE_doit_refuser(self):self._modification('avant_DELETE',False)
    def test_repointage_citation_apres_gardes_avant_DELETE_doit_refuser(self):self._modification('avant_DELETE',True)
