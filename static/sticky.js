window.onscroll = function() {myFunction()};

var navbar = document.getElementsByClassName("navbar")[0];
var sticky = navbar.offsetTop;

function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
}

function rpsc(guess) {
  var bet = document.getElementById("bet").value;
  var enemy = document.getElementById("enemy").value;
  if (bet == "") {
    error = document.getElementById("error")
    error.innerHTML = "You have to enter a bet amount!"
  } else {
    if (enemy == "") {
      error = document.getElementById("error")
      error.innerHTML = "You have to enter the person you want to challenge!"
    } else {
      window.location.href = "https://huge-jasonism.vulcanwm.repl.co/challengerps/" + guess + "/" + enemy + "/" + bet;
    }
  }
}

function rpsac(guess) {
  var pathname = window.location.pathname;
  pathname = pathname.replace("/acceptchallenge/", "")
  window.location.href = "https://huge-jasonism.vulcanwm.repl.co/acceptchallenge/" + pathname + "/" + guess;
}

function cup(guess) {
  var bet = document.getElementById("bet").value;
  window.location.href = "https://huge-jasonism.vulcanwm.repl.co/cupgame/" + guess + "/" + bet;
}

function coin(guess) {
  var bet = document.getElementById("bet").value;
  window.location.href = "https://huge-jasonism.vulcanwm.repl.co/flipcoin/" + guess + "/" + bet;
}

function rps(guess) {
  var bet = document.getElementById("bet").value;
  window.location.href = "https://huge-jasonism.vulcanwm.repl.co/rps/" + guess + "/" + bet;
}

function dice(guess) {
  var bet = document.getElementById("bet").value;
  window.location.href = "https://huge-jasonism.vulcanwm.repl.co/rolldice/" + guess + "/" + bet;
}

function gameredirect(urlpart){
  window.location.href = "https://huge-jasonism.vulcanwm.repl.co" + urlpart;
}

function embedded() {
  try {
    return window.self !== window.top;
  } catch(e) {
    return true;
  }
}

if(embedded()){
  document.body.innerHTML = `<p>Please open this in a <a href="https://huge-jasonism.vulcanwm.repl.co" target="_blank">new tab</a> for best results.`;
}