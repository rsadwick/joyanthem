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
        this.progressInterval;
    },

    load: function(){
         this.player = new YT.Player(this.container, {
            height: '390',
            width: '640',
            videoId: 'P7tu96k_4Uw',
            events: {
                 'onStateChange': this.onPlayerStateChange
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

    onPlayerStateChange: function(event){
        //var scope = this;
        switch(event.data)
		{
			case -1:
				//console.log("Unstarted");
				break;
			case 0:
				//console.log("Ended");
                window.clearInterval(_scope.progressInterval);
				break;
			case 1:
				//console.log("Playing");
                _scope.progressInterval = window.setInterval(_scope.onProgress, 500);

				break;
			case 2:
				//console.log("Paused");
                window.clearInterval(_scope.progressInterval);

				break;
			case 3:
				//console.log("Buffering");

				break;
			case 5:
				//console.log("Cued");
				break;
			default:
				//console.log("UnknownState");
				break;
		}
    },

    onProgress: function(){
        _scope.currentTime = _scope.player.getCurrentTime();
         joy.instance().events.trigger(joy.app.event.ON_VIDEO_PROGRESS, _scope.player.getCurrentTime())
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
        //console.log("video is finished!");
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

//global callback for iframe api - the suck
function onYouTubeIframeAPIReady(e) {
    youtubePlayer.load(e);
}


