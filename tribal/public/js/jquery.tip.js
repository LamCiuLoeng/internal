/**
 * Copyright (c) 2009, Nathan Bubna
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 *
 * Very simple, lightweight tooltip implementation.
 *
 * @version 0.1
 * @name tip
 * @cat Plugins/Tip
 * @author Nathan Bubna
 */
;(function($) {
    var T = $.tip = function(opts) {
        return $('.tip').tip(opts);
    };
    $.fn.tip = function(opts) {
        return this.each(function() {
            var t = $.extend({}, T, opts);
            t.init.call($(this), t);
        });
    };
    $.extend(T, {
        text: undefined,
        tipClass: undefined,
        offset: [3, 3],
        fade: 150,
        html: '<div class="tooltip"></div>',
        get: function(t) { return t.text || this.attr('title'); },
        init: function(t) {
            var self = this.data('tip', t);
            t.create.call(self, t);
            self.hover(function(e) {
                t.show.call(self, t, e);
            }, function() {
                t.hide.call(self, t);
            });
        },
        create: function(t) {
            var txt = t.get.call(this, t);
            t.tip = $(t.html).html(txt).css('position','absolute').hide();
            if (t.tipClass) t.tip.addClass(t.tipClass);
            if (t.css) t.tip.css(t.css);
            $('body').append(t.tip);
            this.removeAttr('title');
            return t.tip;
        },
        position: function(t, pos) { t.tip.css(pos); },
        calc: function(e, t) {
            var tip = t.tip, w = tip.outerWidth(), h = tip.outerHeight(),
                $w = $(window), W = $w.width()+$w.scrollLeft(); H = $w.height()+$w.scrollTop(),
                x = e.pageX + t.offset[0], y = e.pageY + t.offset[1];
            if (x + w > W) x = W - w; // if too far right, move left just enough
            if (y + h > H) y = e.pageY - t.offset[1] - h; // if too far down, move over cursor
            return { left:x, top:y };
        },
        show: function(t, e) {
            //var pos = t.calc.call(this, e, t);
            var pos = {left:this.position().left+this.outerWidth(), top:this.position().top-this.outerHeight()/2-3}
            t.position.call(this, t, pos);
            t.tip.fadeIn(t.fade);
        },
        hide: function(t) { t.tip.fadeOut(t.fade); }
    });

})(jQuery);
