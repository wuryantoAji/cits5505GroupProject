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
    window.location.href = "/application/templates/puzzle_list.html";
  };
});

// jQuery -- AJAX Request

$("#loginForm").submit(function (event) {
  event.preventDefault(); // 阻止表单的默认提交行为

  $.ajax({
    type: "POST",
    url: "/login-register/login_register",
    data: $(this).serialize() + "&action=login", // 添加一个额外的参数来区分登录
    success: function (data) {
      console.log(data);
      if (data.success) {
        window.location.href = "puzzle_list.html"; // jump to puzzle list page after login successfully
      } else {
        alert(data.message); // error message
      }
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
    },
  });
});

$("#signupForm").submit(function (event) {
  event.preventDefault(); // 阻止表单的默认提交行为

  $.ajax({
    type: "POST",
    url: "/login-register/login_register",
    data: $(this).serialize() + "&action=register", // 添加一个额外的参数来区分注册
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
