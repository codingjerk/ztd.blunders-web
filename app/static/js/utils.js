var utils = {};

(function(module) {
    String.prototype.format = function() {
        var str = this;
        for (var i = 0; i < arguments.length; i++) {
            var reg = new RegExp("\\{" + i + "\\}", "gm");
            str = str.replace(reg, arguments[i]);
        }
        return str;
    };

    Number.prototype.pad = function(size) {
        var result = this + "";
        while (result.length < size) result = "0" + result;
        return result;
    };

    Array.prototype.map = function(f, aargs) {
        var args = aargs || [];

        var result = [];
        for (var i = 0; i < this.length; ++i) {
            result.push(f.apply(null, [this[i]].concat(args)));
        }

        return result;
    };

    Array.prototype.mapIndex = function(index, f, args) {
        return this.map(function(e) {
            var result = e;
            result[index] = f(result[index], args);

            return result;
        });
    };

    Array.prototype.extract = function(index) {
        return this.map(function (e) {
            return e[index];
        });
    };

    Array.prototype.filter = function(p, aargs) {
        var args = aargs || [];

        var result = [];
        for (var i = 0; i < this.length; ++i) {
            if (p.apply(null, [this[i]].concat(args))) result.push(this[i]);
        }

        return result;
    };

    Array.prototype.shiftWhile = function(p, aargs) {
        var args = aargs || [];

        var result = [];
        while (this.length > 0) {
            if (!p.apply(null, [this[0]].concat(args))) break;

            result.push(this.shift());
        }

        return result;
    };

    Array.prototype.shiftGroup = function(size) {
        var result = [];
        for (var i = 0; i < size; ++i) {
            result.push(this.shift());
        }

        return result;
    };

    Array.prototype.destructiveChunk = function(groupsize){
        var sets = [], chunks, i = 0;
        chunks = this.length / groupsize;
     
        while(i < chunks){
            sets[i] = this.splice(0,groupsize);
        i++;
        }
        
        return sets;
    };

    Array.prototype.chunk = function (groupsize) {
        var sets = [];
        var chunks = this.length / groupsize;

        for (var i = 0, j = 0; i < chunks; i++, j += groupsize) {
          sets[i] = this.slice(j, j + groupsize);
        }

        return sets;
    };

    module.fixDate = function(rawDate) {
        return new Date(rawDate);
    };

    module.timer = function(interval, callback) {
        if (!callback()) return;

        setTimeout(function() {
            if (!callback()) return;
            module.timer(interval, callback);
        }, interval);
    };

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
    };

    module.escapeHtml = function(text) {
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '$quot;')
            .replace(/'/g, '&#039;')
            .replace(/\n/g, '<br/>');
    };

    module.timePrettyFormat = function(seconds) {
        var mins = Math.floor(seconds / 60);
        var secs = Math.floor(seconds % 60);

        var spentTimeText = mins + ':' + secs.pad(2);

        return spentTimeText;
    };

    module.normalizeTicks = function(ticks, tickSize) {
        var delta = 0;

        for (var i = 1; i < ticks.length; ++i) {
            delta = ticks[i] - ticks[i-1];

            if (delta > tickSize) {
                ticks.splice(i, 0, ticks[i-1] + tickSize);
            }
        }

        ticks.unshift(ticks[0] - tickSize);
        ticks.push(ticks[ticks.length - 1] + tickSize);
    };

    module.generateTooFewDataMessage = function(message) {
        return '<div style="width: 100%; line-height: 300px; font-size: 200%; color: #CCC;' +
            ' text-align: center;">{0}</div>'.format(message);
    };

    module.insertTooFewDataMessage = function(id, message) {
        $('#{0}'.format(id)).html(module.generateTooFewDataMessage(message));
    };
})(utils);

