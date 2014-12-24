(function ($) {
    joy.app = function (canvas) {
        this.events = new joy.eventManager();
        this.canvas = $(canvas);
    };
    joy.app.prototype =
    {
        _captionService: null,
        canvas: null,
        events: null,

        //Service API calls to checkout/shipping
        _getCaptionService: function () {
            if (!this._captionService)
                this._captionService = new joy.Service.FellowShip();
            return this._captionService;
        },

        TemplateFunction: function (config) {
            //do something here
        }
    };

    joy.app.event =
    {
        ON_VIDEO_PROGRESS: 'onVideoProgress'
    };
})(jQuery);