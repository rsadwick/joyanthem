var Video = Class.extend({
    init: function (config) {
        this.config = config;
    },

    load: function(){},

    ready: function(player_id){
        //player is ready for api:
        if (window.CustomEvent) {
          var event = new CustomEvent('onPlayerReady', {detail: {some: 'data'}});
        } else {
          var event = document.createEvent('CustomEvent');
          event.initCustomEvent('onPlayerReady', true, true, {some: 'data'});
        }

        player_id.dispatchEvent(event);
    },

    onProgress: function(e){},

    play: function (){},

    pause: function () {},

    stop: function () {},

    onFinish: function(){},

    setSeek: function(time){},

    getDuration: function(){},

    getSeek: function(){},

    setVolume: function(volume){},

    getVolume: function(){}
});