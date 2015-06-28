(function setupListeners() {
    $('#feedback-button').on('click', function () {
        var textarea = '<textarea placeholder="Enter your message here..."></textarea><br>';
        var sendButton = '<input id="send-button" type="button" value="Send">';

        $('#feedback-container').html('{0}{1}'.format(textarea, sendButton));

        $('#send-button').on('click', function() {
            var message = $('textarea').val();

            if (message.trim().length === 0) {
                notify.error("Can't send empty message");
                return;
            }

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

                $('#feedback-container').html('<span id="thanks">Thanks for your feedback!</span>');
            });
        });
    });

    $('#webmoney-donate').on('click', function() {
        location.href = "http://events.webmoney.ru/social/donate.aspx?groupUID=c60a5228-a142-447e-a57e-ac717065f74e";
    });
})();
