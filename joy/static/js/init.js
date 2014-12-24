(function ($) {
    //todo: check dom for form modals
    jQuery('body').on('click', ".gfc-form-modal", function (e) {
        //call gumby modal
        return false;
    });

    //cache body element to search later
    window.joy.instance(new joy.app
        (
            'body'
        ));


    //all init stuff goes in here
    jQuery(document).ready(function () {
        //var shipping = new joy.template.shipping({ element: '#joy-ship', app: joy.instance() });
        //shipping.somefunction();

        if($('.video').length > 0){
            console.log('caption time')
            captions = new joy.service.captions({element: '#tester', output: '#result', app: joy.instance() });
            captions.getCaptions();
        }

    });

})(jQuery);

