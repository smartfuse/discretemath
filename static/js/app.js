function loadPartial(partial) {
    $.get(partial, function(data) {
        $("#container").html(data);
    });
}

var Router = Backbone.Router.extend({
    routes : {
        "": "welcome",
        "mod_inverse": "extended_gcd",
        "share_secret": "share_secret",
        "reveal_secret": "reveal_secret",
        "encode_error_correction": "encode_error",
        "decode_error_correction": "decode_error",
        "balancing_items": "balancing",
        "recursion": "recursion",
        "*default": "default"
    },
    welcome: function() {
        loadPartial('/static/html/welcome.html');
    },
    extended_gcd: function() {
        loadPartial('/static/html/extended_gcd.html');
    },
    share_secret: function() {
        loadPartial('/static/html/share_secret.html');
    },
    reveal_secret: function() {
        loadPartial('/static/html/reveal_secret.html');
    },
    encode_error: function() {
        loadPartial('/static/html/encode_error.html');
    },
    decode_error: function() {
        loadPartial('/static/html/decode_error.html');
    },
    balancing: function() {
        loadPartial('/static/html/balancing.html');
    },
    recursion: function() {
        loadPartial('/static/html/recursion.html');
    },
    default: function() {
        Backbone.history.navigate("/", true);
    }
});

new Router();
Backbone.history.start({ pushState: true });

jQuery(document).on("click", "a[href]:not([data-bypass])", function(evt) {
    var href = { prop: jQuery(this).prop("href"), attr: jQuery(this).attr("href") };
    var root = location.protocol + "//" + location.host + "/";
    if (href.prop.slice(0, root.length) === root) {
        evt.preventDefault();
        Backbone.history.navigate(href.attr, true);
    }
});
