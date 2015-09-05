var sync = {};

(function initModule(module) {
    var syncTemplate = '<i class="fa fa-circle-o-notch fa-spin"></i>';

    module.ajax = function(args) {
        var syncElement = $('#' + args.id);
        if (syncElement.data('busy')) return;
        syncElement.data('busy', true);

        var savedContent = syncElement.html();

        setTimeout(function() {
            if (!syncElement.data('busy')) return;

            syncElement.data('animated', true);
            syncElement.html(syncTemplate);
        }, 100);

        $.ajax({
            type: args.type || 'POST',
            url: args.url,
            contentType: args.contentType || 'application/json',
            data: JSON.stringify(args.data)
        }).done(function(data) {
            syncElement.data('busy', false);

            if (syncElement.data('animated')) {
                syncElement.html(savedContent);
            }

            args.onDone(data);
        });
    };
})(sync);
