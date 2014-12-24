(function ($) {
    joy.service.captions = function (config) {
        this.app = config.app;
        this.element = $(config.element);
        this.output = $(config.output);
    };

    joy.service.captions.prototype = {
        scope: this,
        secondsToTimecode: function (seconds) {
            var hr  = Math.floor(seconds / 3600);
            var min = Math.floor((seconds - (hr * 3600))/60);
            var sec = Math.floor(seconds - (hr * 3600) -  (min * 60));
            if (hr < 10){ hr    = "0" + hr; }
            if (min < 10){ min = "0" + min; }
            if (sec < 10){ sec  = "0" + sec; }
            if (hr){ hr   = "00"; }

            return hr + ':' + min + ':' + sec + ".000";
        },

        getCaptions: function(){
             var scope = this;
             //get captions
            $.ajax({
                url: "/services/1",
                cache: true,
                success: function(data){
                    scope.setCaptions(data);
                }
            });
        },

        setCaptions: function(captions){
            var scope = this;
            this.element.html(captions)
            //set player up:
            if(this.app.canvas.find("#viemo").length > 0){
                vimeoConfig =  {
                    container: document.getElementById('player1')
                };
                vimeoPlayer = new Vimeo(vimeoConfig);

                vimeoConfig.container.addEventListener('onPlayerReady', function(e){
                    vimeoPlayer.play();

                });

                vimeoConfig.container.addEventListener('onProgress', function(e){
                 var captions = scope.element.webVtt(scope.secondsToTimecode(vimeoPlayer.getSeek()));
                   scope.output.html($(captions).html())

                });
            }
            else if(this.app.canvas.find("#youtube").length > 0){
                var youtubeConfig = {
                    container: document.getElementById('tuba')
                };
                youtubePlayer = new Youtube(youtubeConfig);

                this.app.events.on(
                    joy.app.event.ON_VIDEO_PROGRESS,
                    function (e, eventInfo) {
                        var captions = scope.element.webVtt(scope.secondsToTimecode(youtubePlayer.getSeek()));
                         scope.output.html($(captions).html())
                        },
                    this
                );

                $.getScript( "https://www.youtube.com/iframe_api" );

            }
        }
    }
})(jQuery);