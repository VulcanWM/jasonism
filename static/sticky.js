window.onscroll = function() {myFunction()};

var navbar = document.getElementById("navbar");
var sticky = navbar.offsetTop;

function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
}

function cup(guess) {
  var bet = document.getElementById("bet").value;
  window.location.href = "https://jasonism.vulcanwm.repl.co/cupgame/" + guess + "/" + bet;
}

function coin(guess) {
  var bet = document.getElementById("bet").value;
  window.location.href = "https://jasonism.vulcanwm.repl.co/flipcoin/" + guess + "/" + bet;
}

function rps(guess) {
  var bet = document.getElementById("bet").value;
  window.location.href = "https://jasonism.vulcanwm.repl.co/rps/" + guess + "/" + bet;
}

function dice(guess) {
  var bet = document.getElementById("bet").value;
  window.location.href = "https://jasonism.vulcanwm.repl.co/rolldice/" + guess + "/" + bet;
}

function gameredirect(urlpart){
  window.location.href = "https://jasonism.vulcanwm.repl.co" + urlpart;
}