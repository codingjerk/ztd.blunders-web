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

    Array.prototype.map = function(f) {
        result = [];
        for (var i = 0; i < this.length; ++i) {
            result.push(f(this[i]));
        }

        return result;
    }

    Array.prototype.mapIndex = function(index, f) {
        return this.map(function(e) {
            var result = e;
            result[index] = f(result[index]);

            return e;
        });
    }

    Array.prototype.extract = function(index) {
        return this.map(function (e) {
            return e[index];
        });
    }

    Array.prototype.filter = function(p) {
        var result = [];

        for (var i = 0; i < this.length; ++i) {
            if (p(this[i])) result.push(this[i]);
        }

        return result;
    }

    Array.prototype.shiftWhile = function(p) {
        var result = [];

        while (this.length > 0) {
            if (!p(this[0])) break;

            result.push(this.shift());
        }

        return result;
    }

    module.fixDate = function(rawDate) {
        return new Date(rawDate);
    }
})(utils);