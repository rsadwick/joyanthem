(function ($) {

    var joy = {};
    //template namespace
    joy.service = (joy.service = joy.service || {});

    joy.instance = function (newInstance) {
        if (null != newInstance)
            joy._instance = newInstance;
        return joy._instance;
    };

    //common functions that are needed:
    joy.SomeSharedFunction = function (email) {
        //some something here that is needed for everything
    };

    window.joy = joy;
})(jQuery);