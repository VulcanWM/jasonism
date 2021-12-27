var stop = false;

var i = 0;
function move(time) {
  if (i == 0) {
    i = 1;
    var elem = document.getElementById("myBar");
    var width = 100;
    var id = setInterval(frame, time);
    function frame() {
      if (stop == false) {
        if (width == 0) {
          clearInterval(id);
          stop = true;
          var status = document.getElementById("status")
          status.innerText = 'You lost!'
          i = 0;
        } else {
          width = width - 1;
          elem.style.width = width + "%";
          elem.innerHTML = width + "XP";
        }
      }
    }
  }
}

var i2 = 0;
function move2(time) {
  if (i2 == 0) {
    i2 = 1;
    var elem = document.getElementById("myBar2");
    var width = 100;
    var id = setInterval(frame2, time);
    function frame2() {
      if (stop == false) {
        if (width == 0) {
          clearInterval(id);
          stop = true;
          var status = document.getElementById("status")
          status.innerHTML = 'You won!'
          i = 0;
        } else {
          width = width - 1;
          elem.style.width = width + "%";
          elem.innerHTML = width + "XP";
        }
      }
    }
  }
}