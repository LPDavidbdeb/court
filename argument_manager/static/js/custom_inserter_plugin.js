
tinymce.PluginManager.add('custom_inserter', function(editor, url) {
    const getMenuItems = function() {
        const menuItems = [];
        const narrativeData = window.narrativeData || { events: [], emailQuotes: [], pdfQuotes: [] };

        if (narrativeData.events.length > 0) {
            const eventItems = narrativeData.events.map(function(event) {
                return {
                    type: 'menuitem',
                    text: event.title,
                    onAction: function() {
                        editor.insertContent(`<a href="${event.url}">${event.text}</a>`);
                    }
                };
            });
            menuItems.push({
                type: 'nestedmenuitem',
                text: 'Events',
                getSubmenuItems: function() {
                    return eventItems;
                }
            });
        }

        if (narrativeData.emailQuotes.length > 0) {
            const emailQuoteItems = narrativeData.emailQuotes.map(function(quote) {
                return {
                    type: 'menuitem',
                    text: quote.title,
                    onAction: function() {
                        editor.insertContent(`<a href="${quote.url}">${quote.text}</a>`);
                    }
                };
            });
            menuItems.push({
                type: 'nestedmenuitem',
                text: 'Email Quotes',
                getSubmenuItems: function() {
                    return emailQuoteItems;
                }
            });
        }

        if (narrativeData.pdfQuotes.length > 0) {
            const pdfQuoteItems = narrativeData.pdfQuotes.map(function(quote) {
                return {
                    type: 'menuitem',
                    text: quote.title,
                    onAction: function() {
                        editor.insertContent(`<a href="${quote.url}">${quote.text}</a>`);
                    }
                };
            });
            menuItems.push({
                type: 'nestedmenuitem',
                text: 'PDF Quotes',
                getSubmenuItems: function() {
                    return pdfQuoteItems;
                }
            });
        }

        return menuItems;
    };

    editor.ui.registry.addMenuButton('custom_inserter', {
        icon: 'bookmark',
        tooltip: 'Insert Evidence',
        fetch: function(callback) {
            callback(getMenuItems());
        }
    });

    return {
        getMetadata: function() {
            return {
                name: 'Custom Inserter',
                url: 'https://example.com'
            };
        }
    };
});
