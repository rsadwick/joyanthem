;
(function ($) {

    joy.eventManager = function () {
        this._events = {};
    };

    joy.eventManager.prototype = {
        _events: null,
        on: function (name, handler, scope) {
            this._events[name] = (this._events[name] = this._events[name] || []);
            if (this._events[name].length === 0) {
                this._events[name].push(
                    {
                        handler: handler,
                        scope: scope
                    }
                );
            }
            else {
                var hasEvent = false;
                var eventsByNameLength = this._events[name].length;
                for (var i = 0; i < eventsByNameLength; i++) {
                    if (this._events[name][i].handler === handler && this._events[name][i].scope === scope) {
                        hasEvent = true;
                    }
                }

                if (!hasEvent) {
                    this._events[name].push(
                        {
                            handler: handler,
                            scope: scope
                        }
                    );
                }
            }
        },

        off: function (name, handler, scope) {
            if (!(name in this._events)) {
                return; //didnt find any handler for event
            }
            else {
                this._events[name] = $.grep(this._events[name], function (n) {
                    if ((!handler || n.handler === handler) && (!scope || n.scope === scope)) {
                        return false;
                    }
                    return true;
                });

                if (this._events[name].length == 0) {
                    delete this._events[name];
                }
            }
        },

        trigger: function (name) {
            if (!this._events[name]) {
                return;
            }

            var argumentsCopy = [];
            var argumentsLength = arguments.length;
            for (var i = 0; i < argumentsLength; i++) {
                argumentsCopy[i] = arguments[i];
            }

            var eventsByNameLength = this._events[name].length;
            for (var i = 0; i < eventsByNameLength; i++) {
                this._events[name][i].handler.apply((this._events[name][i].scope || this._events[name][i].handler), argumentsCopy.slice(1));
            }
        }
    };
})(jQuery);