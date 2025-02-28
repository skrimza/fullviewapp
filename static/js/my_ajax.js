$('.form-register').on('submit', function (e) {
    e.preventDefault();
    $.ajax({
        data: JSON.stringify({
            email: $('#email').val(),
            password: $("#password").val()
        }),
        type: 'POST',
        url: '/register',
        contentType: 'application/json', 
        success: function (data) {
            if (data && data.message) {
                $('.output').addClass("active");
                $('.output').text("Теперь войдите").show();
            } else {
                $('.output').addClass("active");
                $('.output').text("Проверьте введённые данные").show();
            }

            $('.form-register')[0].reset();

            setTimeout(function () {
                $('.output').removeClass('active').hide();
            }, 3000);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            // Обработка ошибок AJAX-запроса
            $('.output').text('Проверьте введенные данные').show();
            setTimeout(function () {
                $('.output').removeClass('active').hide();
            }, 3000);
        }
    });
});

$('.form-login').on('submit', function (e) {
    e.preventDefault();
    $.ajax({
        data: JSON.stringify({
            email: $('#login-email').val(),
            password: $("#login-password").val()
        }),
        type: 'POST',
        url: '/login',
        contentType: 'application/json',
        success: function (data) {
            if (data && data.access_token) {
                $('.output').addClass("active");
                $('.output').text("Авторизация Прошла успешно").show();
                localStorage.setItem('token', data.access_token);
            } else {
                $('.output').addClass("active");
                $('.output').text("Проверьте введённые данные").show();
            }
            $('.form-login')[0].reset();
            setTimeout(function () {
                $('.output').removeClass('active').hide();
                $('.form-wrapper').removeClass('active');
                $('.weather-panel').addClass('active');
            }, 3000);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            $('.output').addClass("active");
            $('.output').text(jqXHR.responseJSON?.detail || "Проверьте введённые данные").show();
            $('#modal').addClass('active');
            setTimeout(function () {
                $('.output').removeClass('active').hide();
            }, 3000);
        }
    });
});