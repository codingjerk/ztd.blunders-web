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

    Array.prototype.mapNear = function(index, f) {
        return this.map(function(e) {
            var result = e;
            result[index] = f(result[index]);

            return e;
        });
    }

    module.fixDate = function(rawDate) {
        return new Date(rawDate);
    }
})(utils);