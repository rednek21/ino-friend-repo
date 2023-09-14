
//Скрипт 2
// Проверка пароля на валидность + изменение кнопки
document.addEventListener("DOMContentLoaded", function () {
  var pass1 = document.querySelector(".pass1");
  var pass2 = document.querySelector(".pass2");
  var mail = document.querySelector(".mail");

  pass1.addEventListener("input", checkInput);
  pass2.addEventListener("input", checkInput);
  pass1.addEventListener("input", ErrorColor);
  mail.addEventListener("input", checkInput);

  function checkInput() {
    var computedStyle = getComputedStyle(document.getElementById("errorcolor"));
    if (computedStyle.borderColor === "rgb(0, 128, 0)") {
      changeBackground();
    }
    // Функция для скрытия звездочки
    function Star1() {
      var starSpan = document.getElementById("star1");
      if (pass1.value !== "") {
        starSpan.style.display = "none";
      } else {
        starSpan.style.display = "inline";
      }
    }
    function Star2() {
      var starSpan = document.getElementById("star2");
      if (pass2.value !== "") {
        starSpan.style.display = "none";
      } else {
        starSpan.style.display = "inline";
      }
    }
    function Star3() {
      var starSpan = document.getElementById("star3");
      if (mail.value !== "") {
        starSpan.style.display = "none";
      } else {
        starSpan.style.display = "inline";
      }
    }
    Star1();
    Star2();
    Star3();
  }

  function ErrorColor() {
    if (pass1.value.length < 8 || !isValidPassword(pass1.value)) {
      document.getElementById("errorcolor").style.borderColor = "red";
    } else {
      document.getElementById("errorcolor").style.borderColor = "green";
    }

    // Вызываем функцию changeBackground() после изменения цвета рамки
    changeBackground();
  }

  function changeBackground() {
    if (
      pass1.value === pass2.value &&
      pass1.value !== "" &&
      pass2.value !== ""
    ) {
      document.getElementById("btn_pass").classList.add("btn-primary");
      document.getElementById("btn_pass").classList.remove("btn-secondary");
      document.getElementById("btn_pass").classList.remove("disabled");
    } else {
      document.getElementById("btn_pass").classList.remove("btn-primary");
      document.getElementById("btn_pass").classList.add("disabled");
      document.getElementById("btn_pass").classList.add("btn-secondary");
    }
  }

  function isValidPassword(password) {
    // Проверка наличия заглавной латинской буквы, специального символа, цифры и буквы верхнего регистра, и отсутствия русской буквы
    var regex = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+_!@#$%^&*.,?]).*$/;
    return regex.test(password);
  }
});

// Скрипт 3
//скрипт меняет тип инпута на text, могут быть проблемы со стороны Django.
// В случае возникновения ошибок переписать код
function togglePasswordVisibility(button) {
  var input = button.previousElementSibling;
  var image = button.querySelector("img");

  if (input.type === "password") {
    input.type = "text";
    image.src = "/static/vendor/img/eye-close.svg";
    image.alt = "Скрыть пароль";
  } else {
    input.type = "password";
    image.src = "/static/vendor/img/eye-open.svg";
    image.alt = "Показать пароль";
  }
}
//Скрипт 4
//Валидность почты
document.addEventListener("DOMContentLoaded", function () {
  var login = document.querySelector(".login");
  login.addEventListener("input", changeBackground);

  function changeBackground() {
    if (login.value.includes("@") && login.value.includes(".")) {
      document.getElementById("btn_mail").classList.add("btn-primary");
      document.getElementById("btn_mail").classList.remove("btn-secondary");
      document.getElementById("btn_mail").classList.remove("disabled");
    } else {
      document.getElementById("btn_mail").classList.remove("btn-primary");
      document.getElementById("btn_mail").classList.add("btn-secondary");
      document.getElementById("btn_mail").classList.add("disabled");
    }
    Star1();
  }
  function Star1() {
    var starSpan = document.getElementById("star1");
    if (login.value !== "") {
      starSpan.style.display = "none";
    } else {
      starSpan.style.display = "inline";
    }
    Star1();
  }
});

document.addEventListener("DOMContentLoaded", function () {
  //Бустрап, уведомление о валидности пароля
  const popoverTriggerList = document.querySelectorAll(
    '[data-bs-toggle="popover"]'
  );
  const popoverList = [...popoverTriggerList].map(
    (popoverTriggerEl) => new bootstrap.Popover(popoverTriggerEl)
  );
});

//Скрипт 6
// Изменение кнопки в разделе о нас
document.addEventListener('DOMContentLoaded', function() {
  var name = document.getElementById("mail");
  var mail = document.getElementById("id_email");
  var cringe = document.getElementById("id_message");
  
  name.addEventListener('input', changeBackground);
  mail.addEventListener('input', changeBackground);
  cringe.addEventListener('input', changeBackground);
  
  function changeBackground() {
      if (
        name.value !== "" &&
        mail.value !== "" &&
        cringe.value !== ""
      ) {
        document.getElementById("btn_feed").classList.add("btn-primary");
        document.getElementById("btn_feed").classList.remove("btn-secondary");
        document.getElementById("btn_feed").classList.remove("disabled");
      } else {
        document.getElementById("btn_feed").classList.remove("btn-primary");
        document.getElementById("btn_feed").classList.add("disabled");
        document.getElementById("btn_feed").classList.add("btn-secondary");
      }
    }
})
//Cкрипт 7
// Активность кнопки (вход)
document.addEventListener("DOMContentLoaded", function () {
  var mail = document.querySelector(".mail_entrance");
  var pass = document.querySelector(".pass_entrance");

  mail.addEventListener("input", changeBackground);
  pass.addEventListener("input", changeBackground);

  function changeBackground() {
    if (mail.value !== "" && pass.value !== "") {
      document.getElementById("btn_entrance").classList.add("btn-primary");
      document.getElementById("btn_entrance").classList.remove("btn-secondary");
      document.getElementById("btn_entrance").classList.remove("disabled");
    } else {
      document.getElementById("btn_entrance").classList.remove("btn-primary");
      document.getElementById("btn_entrance").classList.add("disabled");
      document.getElementById("btn_entrance").classList.add("btn-secondary");
    }
  }
});

