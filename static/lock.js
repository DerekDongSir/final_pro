(function (window, document) {
    Miwen = function (code) {
        this.jia = '';
        this.jie =code;
    };
    Miwen.prototype = {
        init: function () {
            this.jiami();
            console.log(this.code);
        },

        jiami: function () {
            var javascr = this.jia;
            var c = String.fromCharCode(javascr.charCodeAt(0) + javascr.length);
            for (var i = 1; i < javascr.length; i++) {
                c += String.fromCharCode(javascr.charCodeAt(i) + javascr.charCodeAt(i - 1));
            }
            this.code = escape(c);
        },

        jiemi: function () {
            var cod = unescape(this.jie);
            var c = String.fromCharCode(cod.charCodeAt(0) - cod.length);
            for (var i = 1; i < cod.length; i++) {
                c += String.fromCharCode(cod.charCodeAt(i) - c.charCodeAt(i - 1));
            }
            eval(c);
        },
    };
    window.Miwen = Miwen
}(window,document));