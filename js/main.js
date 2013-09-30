//= require_self
//= require pages/cpanel_users
//= require pages/repo_admin
//= require pages/group_admin


var app = {};
app._endpoint_handlers = {}

app.endpoint_handler = function(endpoint, func) {
    app._endpoint_handlers[endpoint] = app._endpoint_handlers[endpoint] || []
    app._endpoint_handlers[endpoint].push(func)
}

jQuery(function($) {

    app.endpoint = $('body').data('endpoint');
    var endpoint_handlers = app._endpoint_handlers[app.endpoint] || [];
    $.each(endpoint_handlers, function(i, func) {
        func();
    });
    
});

