(function setupListeners() {
    $('#feedback-button').on('click', function () {
        var textarea = '<textarea placeholder="Enter your message here..."></textarea><br>';
        var sendButton = '<input id="send-button" type="button" value="Send">';

        $('#feedback-container').html('{0}{1}'.format(textarea, sendButton));

        $('#send-button').on('click', function() {
            var message = $('textarea').val();

            $.ajax({
                type: 'POST',
                url: "/api/send-feedback",
                contentType: 'application/json',
                data: JSON.stringify({
                    message: message
                })
            }).done(function(response) {
                if (response.status !== 'ok') {
                    notify.error(response.message);
                    return;
                }

                $('#feedback-container').html('Thanks for your feedback!')
            });
        });
    });
})();