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

    window.location.href = "../../templates/puzzle_list.html";
  };
});

// jQuery -- AJAX Request for login form
$("#loginForm").submit(function (event) {
  event.preventDefault(); // block the default submission of the form

  $.ajax({
    type: "POST",
    url: "/login-register/",
    data: $(this).serialize() + "&form_type=login", // a parameter to distinguish login
    success: function (data) {
      console.log(data);
      if (data.success) {
        window.location.href = "../../templates/puzzle_list.html"; // jump to puzzle list page after login successfully
      } else {
        alert(data.message); // error message
      }
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
    },
  });
});

// jQuery -- AJAX Request for signup form
$("#signupForm").submit(function (event) {
  event.preventDefault(); // block default submission

  $.ajax({
    type: "POST",
    url: "/login-register/",
    data: $(this).serialize() + "&form_type=register", // a parameter to distinguish register
    success: function (data) {
      console.log(data);
      if (data.success) {
        $("#signupModal").hide(); // Hide register modal box
        $("#loginModal").show(); // show login modal box
        alert("Registration successful. Please log in."); // Prompts the user registered successfully and request a login
      } else {
        alert(data.message); // error message
      }
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
    },
  });
});

