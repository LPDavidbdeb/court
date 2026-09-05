/*
 * Formules LaTeX, saisies dans TinyMCE et rendues par KaTeX.
 *
 * Ce que la base contient, et elle seule :
 *
 *     <span class="math-tex">\(\frac{a}{b}\)</span>
 *
 * Le LaTeX est le contenu texte du bloc, délimiteurs compris — pas un
 * attribut. S'il arrivait que la balise saute, la formule resterait lisible et
 * trouvable par une recherche en base plutôt que de disparaître ; et les
 * délimiteurs disent seuls si elle est en ligne — `\(…\)` — ou hors ligne —
 * `\[…\]`, sans qu'il faille un second attribut pour le porter.
 *
 * Le rendu KaTeX, lui, n'entre jamais en base : il se refait à chaque
 * affichage, et se défait avant que l'éditeur ne regarde le bloc. C'est la
 * seule façon sûre ici, parce que les éditeurs sont `inline` : le DOM affiché
 * EST le DOM édité, si bien qu'un rendu laissé en place serait sérialisé tel
 * quel par `getContent()` et écrit en base à la place de la source.
 *
 * D'où les deux moitiés de ce fichier :
 *
 *   1. `rendre` / `derendre`, appelés au chargement de la page et autour de la
 *      vie de chaque éditeur — c'est le plugin qui s'y accroche lui-même, une
 *      page qui le charge n'a rien à orchestrer ;
 *   2. le plugin `maths` proprement dit : un bouton, une boîte de saisie avec
 *      aperçu, et le double-clic qui rouvre une formule existante.
 *
 * La page doit poser `noneditable_class: 'math-tex'` dans sa configuration :
 * pendant l'édition, une formule est un bloc insécable qu'on remplace, jamais
 * un texte où le curseur entre. Le LaTeX tapé à même le texte riche, c'est le
 * `\)` fermant qu'on efface sans le voir.
 */
(function () {
    'use strict';

    var MARQUEUR = 'math-tex';

    // L'ordre compte : `\[` doit être essayé avant `\(`, sans quoi rien, mais
    // la symétrie des deux formes rend l'erreur facile à introduire plus tard.
    var DELIMITEURS = [
        { ouvrant: '\\[', fermant: '\\]', horsLigne: true },
        { ouvrant: '\\(', fermant: '\\)', horsLigne: false }
    ];

    // --- Source et rendu ----------------------------------------------------

    /*
     * Sépare le LaTeX de ses délimiteurs. Les deux bouts sont vérifiés avant
     * d'être coupés : une coupe à l'aveugle sur un bloc qui n'en porte pas
     * mangerait les deux premiers caractères de la formule, et la formule
     * ainsi rognée serait ensuite réenregistrée telle quelle.
     */
    function decouper(texte) {
        var t = texte.trim();
        for (var i = 0; i < DELIMITEURS.length; i++) {
            var d = DELIMITEURS[i];
            if (t.length >= d.ouvrant.length + d.fermant.length &&
                t.indexOf(d.ouvrant) === 0 &&
                t.lastIndexOf(d.fermant) === t.length - d.fermant.length) {
                return {
                    latex: t.slice(d.ouvrant.length, t.length - d.fermant.length),
                    horsLigne: d.horsLigne
                };
            }
        }
        return null;
    }

    function delimiter(latex, horsLigne) {
        var d = DELIMITEURS[horsLigne ? 0 : 1];
        return d.ouvrant + latex + d.fermant;
    }

    /*
     * Pose le rendu dans le bloc et met la source de côté dans `data-tex`.
     * L'attribut est aussi le témoin du rendu : présent, le bloc est rendu ;
     * absent, il porte sa source. `derendre` le retire, si bien qu'il ne
     * peut pas se retrouver en base.
     */
    function rendreUn(span) {
        if (span.dataset.tex !== undefined) return;

        var source = span.textContent;
        var lu = decouper(source);
        // Un bloc sans délimiteurs n'est pas une formule à moitié écrite :
        // c'est un bloc qu'on ne sait pas lire. On le laisse tel quel, visible.
        if (!lu) return;

        span.dataset.tex = source;
        try {
            katex.render(lu.latex, span, {
                displayMode: lu.horsLigne,
                // Une formule fautive s'affiche en rouge, à sa place, et le
                // reste de la page continue de s'afficher. Levée, l'erreur
                // arrêterait le rendu de toutes les formules suivantes.
                throwOnError: false
            });
        } catch (erreur) {
            delete span.dataset.tex;
            span.textContent = source;
            console.error('Formule non rendue :', source, erreur);
        }
    }

    function derendreUn(span) {
        if (span.dataset.tex === undefined) return;
        span.textContent = span.dataset.tex;
        delete span.dataset.tex;
    }

    function surChaqueFormule(racine, action) {
        if (!racine) return;
        Array.prototype.forEach.call(
            racine.querySelectorAll('span.' + MARQUEUR), action);
    }

    function rendre(racine) { surChaqueFormule(racine, rendreUn); }
    function derendre(racine) { surChaqueFormule(racine, derendreUn); }

    // --- Le plugin ----------------------------------------------------------

    function echapper(texte) {
        return texte.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    tinymce.PluginManager.add('maths', function (editor) {

        editor.ui.registry.addIcon('formule',
            '<svg width="24" height="24" viewBox="0 0 24 24">' +
            '<path d="M3 13h3l3 6 5-14h7" fill="none" stroke="currentColor" ' +
            'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>');

        /*
         * Le bloc édité porte sa source, jamais son rendu — voir l'en-tête.
         * Les deux moments sont ceux où le bloc change de main : `init` le
         * prend à l'éditeur, `remove` le rend à la page. Entre les deux,
         * `getContent()` ne peut voir que du LaTeX.
         */
        editor.on('init', function () { derendre(editor.getBody()); });
        editor.on('remove', function () { rendre(editor.getBody()); });

        function formuleSousLeCurseur() {
            var noeud = editor.selection.getNode();
            return noeud && noeud.closest ? noeud.closest('span.' + MARQUEUR) : null;
        }

        function ouvrirBoite(cible) {
            var lu = cible ? decouper(cible.textContent) : null;

            editor.windowManager.open({
                title: 'Formule',
                size: 'normal',
                initialData: {
                    latex: lu ? lu.latex : '',
                    horsLigne: lu ? lu.horsLigne : false
                },
                body: {
                    type: 'panel',
                    items: [
                        { type: 'textarea', name: 'latex', label: 'LaTeX', maximized: true },
                        { type: 'checkbox', name: 'horsLigne', label: 'Hors ligne (centrée sur sa propre ligne)' },
                        { type: 'htmlpanel', html: '<label class="tox-label">Aperçu</label>' +
                            '<div id="apercu-maths" style="min-height:3rem;padding:.5rem;' +
                            'border:1px solid rgba(34,47,62,.2);border-radius:3px;overflow-x:auto"></div>' }
                    ]
                },
                buttons: [
                    { type: 'cancel', text: 'Annuler' },
                    { type: 'submit', text: cible ? 'Remplacer' : 'Insérer', primary: true }
                ],

                onChange: function (api) { apercu(api.getData()); },

                onSubmit: function (api) {
                    var donnees = api.getData();
                    var latex = donnees.latex.trim();
                    if (!latex) { api.close(); return; }

                    var source = delimiter(latex, donnees.horsLigne);
                    if (cible) {
                        // Le bloc existe déjà : on remplace son texte, sans
                        // toucher au reste du document ni à la sélection.
                        cible.textContent = source;
                    } else {
                        editor.insertContent(
                            '<span class="' + MARQUEUR + '">' + echapper(source) + '</span>&nbsp;');
                    }
                    editor.setDirty(true);
                    api.close();
                }
            });

            apercu({ latex: lu ? lu.latex : '', horsLigne: lu ? lu.horsLigne : false });
        }

        function apercu(donnees) {
            var zone = document.getElementById('apercu-maths');
            if (!zone) return;
            try {
                katex.render(donnees.latex || '', zone, {
                    displayMode: donnees.horsLigne,
                    throwOnError: false
                });
            } catch (erreur) {
                zone.textContent = String(erreur);
            }
        }

        editor.ui.registry.addButton('maths', {
            icon: 'formule',
            tooltip: 'Formule (LaTeX)',
            onAction: function () { ouvrirBoite(formuleSousLeCurseur()); }
        });

        editor.ui.registry.addMenuItem('maths', {
            icon: 'formule',
            text: 'Formule…',
            onAction: function () { ouvrirBoite(formuleSousLeCurseur()); }
        });

        // Une formule est insécable pendant l'édition : le double-clic est le
        // seul chemin vers son contenu.
        editor.on('dblclick', function () {
            var cible = formuleSousLeCurseur();
            if (cible) ouvrirBoite(cible);
        });

        return { getMetadata: function () { return { name: 'Formules LaTeX (KaTeX)' }; } };
    });

    // Au chargement : les formules déjà en page. Les éditeurs, eux, n'existent
    // pas encore — ils s'ouvrent au clic, et se chargent alors de se défaire
    // du rendu par le crochet `init` ci-dessus.
    document.addEventListener('DOMContentLoaded', function () { rendre(document); });

    // Exposé pour le contenu arrivé après coup (une réponse AJAX, un bloc
    // réaffiché) et pour le garde-fou d'enregistrement.
    window.Maths = { rendre: rendre, derendre: derendre, MARQUEUR: MARQUEUR };
})();
