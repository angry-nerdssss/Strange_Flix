
var player=videojs('videoPlayer',{
	autoplay:'unmuted',
	controls:true,
	loop:true,
	playbackRates:[0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0],
});
player.ready(function() {
  this.hotkeys({
    volumeStep: 0.1,
    seekStep: 10,
    enableModifiersForNumbers: false
  });
});
