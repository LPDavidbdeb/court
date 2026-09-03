/*
 * Menu d'insertion de citations pour TinyMCE.
 *
 * Le serveur renvoie une liste ordonnée de groupes ; une entrée est soit un
 * élément qu'on insère (`titre` + `valeur`), soit un sous-groupe (`titre` +
 * `entrees`). Ce fichier ne connaît pas la profondeur du menu : il rend ce
 * qu'on lui donne, récursivement. Toute la mise en forme du menu se décide
 * dans `argument_manager.views.all_quotes_list_for_tinymce`.
 */
tinymce.PluginManager.add('custom_inserter', function (editor) {

    // L'identité de la page se lit dans le bloc que l'éditeur occupe :
    // « /texte/email_manager/emailthread/66/note/ ». Aucun gabarit n'a eu à
    // être modifié pour cela — tous les blocs éditables portent déjà cette
    // adresse. Quand l'éditeur vise autre chose qu'un bloc éditable (les
    // formulaires de parjure et de contestation visent un <textarea>), il n'y
    // a pas de contexte et le menu retombe sur les listes générales.
    function parametresDeContexte() {
        const cible = editor.targetElm;
        const url = cible && cible.dataset ? cible.dataset.url : null;
        const trouve = url ? url.match(/^\/texte\/([^/]+)\/([^/]+)\/(\d+)\//) : null;
        if (!trouve) return '';
        return '?app=' + encodeURIComponent(trouve[1]) +
               '&modele=' + encodeURIComponent(trouve[2]) +
               '&pk=' + encodeURIComponent(trouve[3]);
    }

    function enElementsDeMenu(entrees) {
        return entrees.map(function (entree) {
            if (entree.entrees) {
                return {
                    type: 'nestedmenuitem',
                    text: entree.titre,
                    getSubmenuItems: function () { return enElementsDeMenu(entree.entrees); }
                };
            }
            return {
                type: 'menuitem',
                text: entree.titre,
                onAction: function () { editor.insertContent(entree.valeur); }
            };
        });
    }

    editor.ui.registry.addMenuButton('custom_inserter', {
        icon: 'bookmark',
        tooltip: 'Insert Evidence',
        fetch: function (callback) {
            fetch('/arguments/ajax/all-quotes-for-tinymce/' + parametresDeContexte())
                .then(function (reponse) {
                    if (!reponse.ok) throw new Error('HTTP ' + reponse.status);
                    return reponse.json();
                })
                .then(function (groupes) { callback(enElementsDeMenu(groupes)); })
                .catch(function (erreur) {
                    // Un menu vide ne dit pas s'il n'y a rien à insérer ou si
                    // l'appel a échoué. La ligne inerte, elle, le dit.
                    console.error('Citations : chargement impossible', erreur);
                    callback([{ type: 'menuitem', text: 'Citations indisponibles', enabled: false }]);
                });
        }
    });

    return {
        getMetadata: function () {
            return { name: 'Custom Inserter', url: 'https://example.com' };
        }
    };
});
