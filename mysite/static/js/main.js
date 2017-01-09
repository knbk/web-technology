var bloodhound;

jQuery(document).ready(function($) {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js').then(function(registration) {
            // Registration was successful
            console.log('ServiceWorker registration successful with scope: ', registration.scope);
        }).catch(function(err) {
            // registration failed :(
            console.log('ServiceWorker registration failed: ', err);
        });
    } else {
        console.log('Browser does not support ServiceWorker');
        return;
    }

    var CACHE_NAME = 'sw-cache';
    $('#clear-cache').click(function() {
        caches.open(CACHE_NAME).then(function(cache) {
            cache.keys().then(function(keyList) {
                console.log('Deleting keys...');
                console.log(keyList);
            })
        });
        caches.delete(CACHE_NAME);
    });

    $('#download').click(function() {
        var spinner = $('#download-spinner');
        if (spinner.is(':visible')) {
            // We're already fetching the response...
            return;
        }
        var url = window.location.href;
        var glyph = $('#download');
        var isSaved = glyph.hasClass('saved');
        var request = new Request(url);

        console.log(url);
        console.log(isSaved);

        if (!isSaved) {
            spinner.removeClass('hidden');
            caches.open(CACHE_NAME).then(function(cache) {
                console.log("Adding request to cache: ", request.url);
                cache.add(request).then(function() {
                    console.log("Added request to cache");
                    spinner.addClass('hidden');
                    glyph.addClass('saved');
                });
            });
        } else {
            glyph.removeClass('glyphicon-remove');
            glyph.addClass('glyphicon-download');
            caches.open(CACHE_NAME).then(function(cache) {
                console.log("Removing request from cache: ", request.url);
                cache.delete(request).then(function() {
                    glyph.removeClass('saved');
                });
            });
        }
    });

    $('#download').hover(function() {
        if ($(this).hasClass('saved')) {
            $(this).removeClass('glyphicon-download');
            $(this).addClass('glyphicon-remove');
        }
    }, function() {
        $(this).removeClass('glyphicon-remove');
        $(this).addClass('glyphicon-download');
    });

    (function() {
        var url = window.location.href;
        var glyph = $('#download');
        var request = new Request(url);
        caches.open(CACHE_NAME).then(function(cache) {
            cache.match(request).then(function(response) {
                if (response) {
                    console.log('Found a response matching ', url);
                    glyph.addClass('saved');
                }
            })
        })
    })();


    (function() {
        var host = window.location.host;
        var protocol = window.location.protocol;
        var getUrl = function(path) {return protocol + '//' + host + path};
        var songdata = {
            'wander navarone': {"title":"Wander","artist":"Navarone","url": getUrl("/songs/navarone-wander.html")},
            'hallelujah leonard cohen': {"title":"Hallelujah","artist":"Leonard Cohen","url": getUrl("/songs/leonard-cohen-hallelujah.html")},
            'uptown funk bruno mars': {"title":"Uptown Funk","artist": "Bruno Mars", "url": getUrl("/songs/bruno-mars-uptown-funk.html")},
            'end has a start editors': {"title": "End Has a Start","artist": "The Editors", "url": getUrl("/songs/editors-end-has-a-start.html")},
            'house of the rising sun animals': {"title": "The House of the Rising Sun", "artist": "The Animals", "url": getUrl("/songs/the-animals-house-of-the-rising-sun.html")},
            'something from nothing foo fighters': {"title": "Something From Nothing", "artist": "Foo Fighters", "url": getUrl("/songs/foo-fighters-something-from-nothing.html")},
            "from can to can't corey taylor": {"title": "From Can To Can't", "artist": "Corey Taylor", "url": getUrl("/songs/corey-taylor-from-can-to-cant.html")},
        };
        var songs = [
            "wander navarone",
            "hallelujah leonard cohen",
            "uptown funk bruno mars",
            "end has a start editors",
            "house of the rising sun animals",
            "something from nothing foo fighters",
            "from can to can't corey taylor",
        ];
        bloodhound = new Bloodhound({
            datumTokenizer: Bloodhound.tokenizers.whitespace,
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            // identify: function(obj) {return obj.title},
            // prefetch: '/songs/songs.json'
            local: songs
        });
        function bloodhoundWithDefaults(q, sync) {
            if (q === '') {
                sync(bloodhound.get(
                    'wander navarone',
                    'hallelujah leonard cohen',
                    'uptown funk bruno mars',
                    "end has a start editors",
                    "house of the rising sun animals"
                ));
            }

            else {
                bloodhound.search(q, sync);
            }
        }
        $('.typeahead').typeahead({
            hint: true,
            highlight: true,
            minLength: 0
        }, {
            name: 'urls',
            source: bloodhoundWithDefaults,
            // displayKey: 'title'
            templates: {
                suggestion: function(obj) {
                    console.log(obj);
                    song = songdata[obj];
                    return $('<a href="' + song.url + '"><span>' + song.title + ' -- ' + song.artist + '</span></a>');
                }
            }

        });
        // $('#srch-term-main').typeahead({
        //     hint: true,
        //     highlight: true,
        //     minLength: 0
        // }, {
        //     name: 'urls',
        //     source: bloodhoundWithDefaults,
        //     // displayKey: 'title'
        //     templates: {
        //         suggestion: function(obj) {
        //             console.log(obj);
        //             song = songdata[obj];
        //             return $('<div><a href="' + song.url + '">' + song.title + ' -- ' + song.artist + '</a></div>');
        //         }
        //     }
        //
        // });
    })();
});