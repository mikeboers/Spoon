app.endpoint_handler('account', function() {

    $('form.git-account-delete').each(function() {
        var $form = $(this);
        var name = $form.data('account-name');
        var prompt = "DELETE " + name;
        $form.formIsDangerous({
            message: 'This can <strong>NOT</strong> be undone.<br/>If you are sure, type <code>' + prompt + '</code>.',
            prompt: prompt,
        });
    });

});
