/* Youtube class
 * iFrame api
 * */

var Youtube = Video.extend({
    //config override and element
    init: function (config) {
        _scope = this;
        this.config = config;
        this.container = this.config.container;
        this.currentTime = 0;
        this.duration = 0;
    },

    load: function(){
         this.player = new YT.Player(this.container, {
            height: '390',
            width: '640',
            videoId: 'P7tu96k_4Uw',
            events: {

            },
            playerVars: {
                'html5': 1,
                'theme': 'light',
                'modestbranding': 1,
                'showinfo': 0,
                'showsearch': 0,
                'rel': 0,
                'controls': 1,
                'wmode': 'transparent',
                'cc_load_policy': 1
            }
        });
    },

    ready: function(player_id){
        this.duration = _scope.player.getDuration();
       // setInterval(_scope.onProgress, 250);
        //_scope.onProgress();
        console.log(player_id)
        this._super(_scope.container);
    },

    onProgress: function(){
        _scope.currentTime = _scope.player.getCurrentTime();
    },

    onPause: function(e){

    },

    play: function () {
        if(this.player)
            this.player.playVideo();
    },

    pause: function () {
        this.player.pauseVideo();
    },

    stop: function () {
        this.player.stopVideo();
    },

    onFinish: function(){
        console.log("video is finished!");
    },

    getDuration: function(){

        return this.duration;
    },

    setSeek: function(time){
        this.player.seekTo(time);
    },

    getSeek: function(){
        return this.currentTime;
    },

    setVolume: function(volume){
        this.player.setVolume(volume);
    }
});


