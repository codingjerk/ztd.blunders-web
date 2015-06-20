var notify = {};

(function initModule(module) {
    $.notify.addStyle('error', {
      html: "<div><i class='fa fa-exclamation-circle'></i> <span data-notify-text/></div>",
      classes: {
        base: {
            "color": "#ffffff",
            "border-color": "rgb(212, 63, 58)",
            "background-color": "rgb(217, 83, 79)",
            "padding": "7px 15px",
            "margin-bottom": "15px",
            "margin-right": "55px",
            "border-radius": "4px",
            "border-style": "solid",
            "border-width": "1px",
        }
      }
    });

    module.error = function(text) {
        if (text === undefined) return;

        $.notify(
            text, 
            {
                style: 'error',
                position: 'bottom right',
            }
        );
    }

    $.notify.addStyle('inplace-error', {
      html: "<div><i class='fa fa-exclamation-circle'></i> <span data-notify-text/></div>",
      classes: {
        base: {
            "color": "#ffffff",
            "border-color": "rgb(212, 63, 58)",
            "background-color": "rgb(217, 83, 79)",
            "padding": "7px 15px",
            "border-radius": "4px",
            "border-style": "solid",
            "border-width": "1px",
            "white-space": "nowrap"
        }
      }
    });

    module.inplaceError = function(id, text) {
        if (text === undefined) return;

        $('#' + id).notify(
            text, 
            {
                style: 'inplace-error',
                position: 'right middle',
            }
        );
    }
})(notify);