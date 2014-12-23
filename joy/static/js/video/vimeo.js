/* Vimeo class
 * Depends on froogaloop
 * */
var Vimeo = Video.extend({
    //config override and element

    init: function (config) {
        _scope = this;
        this.config = config;
        this.player = this.config.container;
        this.currentTime = 0;
        this.duration = 0;
        this.onProgressEvent;
        //froogaloop dependancy
        $f(this.player).addEvent('ready', this.ready);
    },

    load: function(){},

    ready: function(player_id){

        froogaloop = $f(player_id);
        froogaloop.addEvent('playProgress', _scope.onProgress)
        froogaloop.addEvent('pause', _scope.onPause);
        froogaloop.addEvent('finish', _scope.onFinish);
        froogaloop.api('getDuration', function (value) {
            _scope.duration = value;
        });
        console.log(player_id);
        onProgressEvent = new Event('onProgress');
        this._super(_scope.player);

    },

    onProgress: function(e){
        _scope.currentTime = e;
        _scope.player.dispatchEvent(onProgressEvent);
    },

    onPause: function(e){
        console.log("paused");
    },

    play: function () {
        froogaloop.api('play');
    },

    pause: function () {
        froogaloop.api('pause');
    },

    stop: function () {
        froogaloop.api('unload');
    },

    onFinish: function(){
        console.log("video is finished!");
    },

    getDuration: function(){

        return this.duration;
    },

    setSeek: function(time){
         froogaloop.api('seekTo', time);
    },

    getSeek: function(){
        return this.currentTime.seconds;
    },

    setVolume: function(volume){
        froogaloop.api('setVolume', volume);
    }
});