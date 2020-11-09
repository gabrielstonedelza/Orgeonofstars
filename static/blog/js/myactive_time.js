monitor_dtime()
function monitor_dtime(){
// Set the date we're counting down to
var mydate = new Date()
var next30min = mydate.getMinutes() + 60
mydate.setMinutes(next30min)
var mydtime = mydate.getTime()

var x = setInterval(function() {

  var now = new Date().getTime();
    
  var distance = mydtime - now;

  if (distance < 0) {
    // window.location.replace("https://connectdjango.com/logout/")
    // window.location.replace("http://127.0.0.1:8000/logout/")
    window.location.replace("https://orgeonofstars.org/logout/")
  }
}, 1000);
}
