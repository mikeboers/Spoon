/*

each(function() {
        var $this = $(this);
        console.log(this);
        $this.click(function(e) {
            e.preventDefault();
            vex.dialog.confirm({
                message: 'Are you sure? This cannot be undone!',
                callback: function(res) {
                    if (res) {
                        $this.closest('form').submit();
                    }
                }
            });
        });
    });

*/

(function($) {

$.fn.formIsDangerous = function(opts) {

    opts = $.extend({}, $.fn.formIsDangerous.defaults, opts);

    var $form = $(this);

    var submit = function() {
        $('<input />', {type: 'hidden', name: 'user_accepted_danger', value: '1'})
            .appendTo($form);
        $form[0].submit();
    }

    $form.submit(function(e) {

        e.preventDefault();

        if (opts.prompt) {
            vex.dialog.prompt({
                message: opts.message,
                callback: function(res) {
                    if (res == opts.prompt) {
                        submit();
                    } else if (res) {
                        vex.dialog.alert("It didn't match. It must be a sign.");
                    }
                }
            })
        } else {
            vex.dialog.confirm({
                message: opts.message,
                callback: function(res) {
                    if (res) {
                        submit();
                    }
                }
            });
        }

    });

}

$.fn.formIsDangerous.defaults = {
    message: 'This action is very dangerous. Are you sure?',
    promp: undefined,
};

})(jQuery);
