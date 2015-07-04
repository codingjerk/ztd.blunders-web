var sync = {};

(function initModule(module) {
	var syncTemplate = '<i class="fa fa-circle-o-notch fa-spin"></i>';

	module.ajax = function(args) {
		var syncElement = $('#' + args.id);
		if (syncElement.data('busy')) return;
		syncElement.data('busy', true);

		var savedContent = syncElement.html();

		syncElement.html(syncTemplate);

        $.ajax({
        	type: args.type || 'POST',
            url: args.url,
            contentType: args.contentType || 'application/json',
            data: JSON.stringify(args.data)
        }).done(function(data) {
        	syncElement.html(savedContent);  
			syncElement.data('busy', false);

        	args.onDone(data);
        });
	};
})(sync);