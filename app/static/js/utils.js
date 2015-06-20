var utils = {};

(function(module) {
    String.prototype.format = function() {
        var str = this;
        for (var i = 0; i < arguments.length; i++) {
            var reg = new RegExp("\\{" + i + "\\}", "gm");
            str = str.replace(reg, arguments[i]);
        }
        return str;
    }

    Number.prototype.pad = function(size) {
        var result = this + "";
        while (result.length < size) result = "0" + result;
        return result;
    }

    Array.prototype.map = function(f, args) {
        var args = args || [];

        var result = [];
        for (var i = 0; i < this.length; ++i) {
            result.push(f.apply(null, [this[i]].concat(args)));
        }

        return result;
    }

    Array.prototype.mapIndex = function(index, f, args) {
        return this.map(function(e) {
            var result = e;
            result[index] = f(result[index], args);

            return result;
        });
    }

    Array.prototype.extract = function(index) {
        return this.map(function (e) {
            return e[index];
        });
    }

    Array.prototype.filter = function(p, args) {
        var args = args || [];

        var result = [];
        for (var i = 0; i < this.length; ++i) {
            if (p.apply(null, [this[i]].concat(args))) result.push(this[i]);
        }

        return result;
    }

    Array.prototype.shiftWhile = function(p, args) {
        var args = args || [];

        var result = [];
        while (this.length > 0) {
            if (!p.apply(null, [this[0]].concat(args))) break;

            result.push(this.shift());
        }

        return result;
    }

    Array.prototype.shiftGroup = function(size) {
        var result = [];
        for (var i = 0; i < size; ++i) {
            result.push(this.shift());
        }

        return result;
    }

    module.fixDate = function(rawDate) {
        return new Date(rawDate);
    }

    module.timer = function(interval, callback) {
        setTimeout(function() {
            if (!callback()) return;
            module.timer(interval, callback);
        }, interval);
    }

    module.counter = function(interval, tickCallback) {
        var that = {
            startTime: null,
            enabled: false,
            
            tick: tickCallback,

            total: function () {
                var secondsFromStart = (new Date() - that.startTime) / 1000;
                return Math.round(secondsFromStart);
            },

            start: function () {
                that.startTime = new Date();
                that.enabled = true;

                module.timer(interval, function () {
                    if (!that.enabled) return false;

                    that.tick();

                    return true;
                });
            },

            stop: function () {
                that.enabled = false;
            }
        };

        return that;
    }

    module.escapeHtml = function(text) {
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '$quot;')
            .replace(/'/g, '&#039;')
            .replace(/\n/g, '<br/>');
    }
})(utils);