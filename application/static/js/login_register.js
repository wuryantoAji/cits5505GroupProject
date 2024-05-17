document.addEventListener("DOMContentLoaded", function () {
  console.log("Script loaded and executed");
  var loginModal = document.getElementById("loginModal");
  var signupModal = document.getElementById("signupModal");

  var loginBtn = document.querySelector(".login_button");
  var signupBtn = document.querySelector(".signup_button");
  var guestBtn = document.querySelector(".guest_button");

  var loginClose = document.querySelector(".loginClose");
  var signupClose = document.querySelector(".signupClose");

  loginBtn.onclick = function () {
    loginModal.style.display = "block";
  };

  signupBtn.onclick = function () {
    signupModal.style.display = "block";
  };

  loginClose.onclick = function () {
    loginModal.style.display = "none";
  };

  signupClose.onclick = function () {
    signupModal.style.display = "none";
  };

  window.onclick = function (event) {
    if (event.target == loginModal) {
      loginModal.style.display = "none";
    }
    if (event.target == signupModal) {
      signupModal.style.display = "none";
    }
  };

  // Redirect to game page if Guest button is clicked
  guestBtn.onclick = function () {
    window.location.href = "/puzzle-list/";
  };
});

// jQuery -- AJAX Request

$("#loginForm").submit(function (event) {
  event.preventDefault(); // block the default submission of the form
  document.getElementById('loginForm').submit();
});

$("#signupForm").submit(function (event) {
  event.preventDefault(); // blcok default submission
  document.getElementById('signupForm').submit();
});
