(function setupListeners() {
    $('#logout-button').on('click', function () {
        sync.ajax({
            id: 'logout-icon',
            url: '/logout',
            data: {},
            onDone: function(data) {
                if (data.status !== 'ok') {
                    notify.error(data.message);               
                    return;
                }

                location.reload();
            }
        });
    });

})();