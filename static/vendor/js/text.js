// //Скрипт 1
// //Уведомление об ошибке(пароль повторяется)
// function toastON_newpass() {
//   // var element = document.getElementById("myToast");
//   const pass_auth = false;

//   // Отправляем JSON-данные на сервер
//   $.ajax({
//       type: 'POST',
//       url: '/handle_pass_auth/',  // Здесь укажи путь к вашему обработчику
//       data: {
//           pass_auth: pass_auth
//       },
//       success: function(response) {
//           if (response.valid) {
//               showSuccessToast();
//           } else {
//               showErrorToast();
//           }
//       },
//       error: function(error) {
//           console.error(error);
//           // Другие действия при ошибке
//       }
//   });
// }

// function showSuccessToast() {
//   var element = document.getElementById("myToast");
//   var myToast = new bootstrap.Toast(element);
//   myToast.show();
// }

// function showErrorToast() {
//   var element = document.getElementById("myToast");
//   element.style.borderColor = "red";
//   document.getElementById("text-error").innerHTML = "Пароль не может быть изменен на старый.";
//   var myToast = new bootstrap.Toast(element);
//   myToast.show();
// }

//  //Скрипт 2 
// //Успешное сообщение после ввода почты
// function toastON_mail() {
//   const mail_auth = false;

//   // Отправляем JSON-данные на сервер
//   $.ajax({
//       type: 'POST',
//       url: '/handle_mail_auth/',  // Здесь укажи путь к обработчику
//       data: {
//           mail_auth: mail_auth
//       },
//       success: function(response) {
//           if (response.valid) {
//               showSuccessToast();
//           } else {
//               showErrorToast();
//           }
//       },
//       error: function(error) {
//           console.error(error);
//           // Другие действия при ошибке
//       }
//   });
// }

// function showSuccessToast() {
//   var element = document.getElementById("toast_mail");
//   var myToast = new bootstrap.Toast(element);
//   myToast.show();
// }

// function showErrorToast() {
//   var element = document.getElementById("toast_mail");
//   document.getElementById("toast_mail").style.borderColor = "red";
//   document.getElementById("text-error").innerHTML = "Указанная почта Отсутствует в системе";
//   var myToast = new bootstrap.Toast(element);
//   myToast.show();
// }

// //Скрипт 3 (отправка данных при входе на сервер и возврат значения)
// //В случае если не валид показываем тост, иначе пускаем в аккаунт
// function toastON_entrance() {
//   // var element = document.getElementById("toast_entrance");

//   // Получите значения логина и пароля, например, из соответствующих input-полей
//   var login = document.getElementById("login_input").value;
//   var password = document.getElementById("password_input").value;

//   // Отправляем JSON-данные на сервер
//   $.ajax({
//       type: 'POST',
//       url: "{% url 'users:login' %}",  // Здесь укажите путь к вашему обработчику
//       data: {
//           login: login,
//           password: password
//       },
//       success: function(response) {
//           if (response.valid === 1) {
//               // В случае успешной авторизации, выполните действия для входа в аккаунт
//               // Например, перенаправление на другую страницу
//               window.location.href = "{% url 'users:profile' user.id %}";
//           } else {
//               showErrorToast();
//           }
//       },
//       error: function(error) {
//           console.error(error);
//           // Другие действия при ошибке
//       }
//   });
// }

// function showErrorToast() {
//   var element = document.getElementById("toast_entrance");
//   element.style.borderColor = "red";

//   var myToast = new bootstrap.Toast(element);
//   myToast.show();
// }
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
// //Скрипт 5
// //Успешное сообщение после ввода почты
// function toastON_mail() {
//   var element = document.getElementById("toast_mail");
//   //Строка ниже отвечает за уведомление об ошибке
//   //Параметр mail_auth необходимо передавать через JSON, допишем по ходу работы
//   const mail_auth = false;
//   if (!mail_auth) {
//     document.getElementById("toast_mail").style.borderColor = "red";
//     document.getElementById("text-error").innerHTML =
//       "Указанная почта Отсутствует в системе";
//   }
//   // Create toast instance
//   var myToast = new bootstrap.Toast(element);
//   myToast.show();
// }

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
// //Скрипт 5
// //Почта уже зарегистрирована в системе

// function toastON_reg() {
//   var element = document.getElementById("toast_reg");
//   //Строка ниже отвечает за уведомление об ошибке
//   //Параметр pass_auth необходимо передавать через JSON, допишем по ходу работы
//   //будем передавать код ошибки и уже по нему запускать нужный скрипт
//   const mail_auth = false;
//   if (mail_auth == true) {
//     element.style.borderColor = "red";
//     document.getElementById("text-error").innerHTML =
//       "Указанная почта уже зарегистрирована в системе";
//     // Create toast instance
//   } else {
//     element.style.borderColor = "red";
//     document.getElementById("text-error").innerHTML = "Почта указана неверно";
//   }
//   var myToast = new bootstrap.Toast(element);
//   myToast.show();
// }

// //Скрипт 6 Куки
// function setCookie(name, value, days) {
//   let expires = "";
//   if (days) {
//     let date = new Date();
//     date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
//     expires = "; expires=" + date.toUTCString();
//   }
//   document.cookie = name + "=" + (value || "") + expires + "; path=/";
// }

// function getCookie(name) {
//   let matches = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"));
//   return matches ? decodeURIComponent(matches[1]) : undefined;
// }

// // Wait for the DOMContentLoaded event
// document.addEventListener('DOMContentLoaded', function() {

//   // Create the HTML for the cookie note
//   let cookieNoteHTML = `
//     <div id="cookie_note">
//       <p>
//         Мы используем файлы cookies для улучшения работы сайта. Оставаясь на
//         нашем сайте, вы соглашаетесь с условиями использования файлов cookies.
//         Чтобы ознакомиться с нашими Положениями о конфиденциальности и об
//         использовании файлов cookie,
//         <a href="{% url 'ino_main:cookie' %}" id="redirect_link" target="">нажмите здесь</a>

//       </p>
//       <button class="button cookie_accept btn btn-primary btn-sm">
//         Я согласен
//       </button>
//     </div>
//   `;

//   // Insert the cookie note HTML into the document before the end of the body
//   document.body.insertAdjacentHTML('beforeend', cookieNoteHTML);

//   let cookieNote = document.getElementById('cookie_note');
//   let cookieBtnAccept = cookieNote.querySelector('.cookie_accept');

//   // Если куки cookies_policy нет или она просрочена, то показываем уведомление
//   if (!getCookie('cookies_policy')) {
//     cookieNote.classList.add('show');
//   }

//   // При клике на кнопку устанавливаем куку cookies_policy на один год
//   cookieBtnAccept.addEventListener('click', function () {
//     setCookie('cookies_policy', 'true', 365);
//     cookieNote.classList.remove('show');
//   });
// });


