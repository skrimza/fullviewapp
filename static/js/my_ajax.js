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


$('.weather-request').on('submit', function (e) {
    e.preventDefault();
    var myToken = localStorage.getItem('token');
    if (!myToken) {
        $('.output').addClass("active").text("Пожалуйста, авторизуйтесь").show();
        setTimeout(function () {
            $('.output').removeClass('active').hide();
        }, 3000);
        return;
    }
    $.ajax({
        url: '/weather?' + $.param({
            day: $('#day-select').val(),
            city: $('#city').val()
        }),
        type: 'GET',
        headers: {
            "Authorization": "Bearer " + myToken
        },
        success: function (response) {
            $('.weather-table').replaceWith(response);  // Обновляем только таблицу
            $('.output').addClass("active").text("Погода успешно обновлена").show();
            setTimeout(function () {
                $('.output').removeClass('active').hide();
            }, 3000);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            $('.output').addClass("active").text("Ошибка при запросе погоды").show();
            setTimeout(function () {
                $('.output').removeClass('active').hide();
            }, 3000);
        }
    });
});

$(document).on('click', '.weather-panel-close', function () {
    $('.weather-panel').removeClass('active');
});

$(document).on('click', '.form-wrapper-close', function () {
    $('.form-wrapper').removeClass('active');
});
$(document).on('click', '.weather-data-close', function () {
    $('.data-weather').removeClass('active');
});

$(document).on('click', '.form-btn', function () {
    var token = localStorage.getItem('token');
    if (token) {
        $('.weather-panel').addClass('active');
    } else {
        $('.form-wrapper').addClass('active');
    }
});

$(document).on('click', '.data-link', function () {
    var myToken = localStorage.getItem('token');
    if (!myToken) {
        $('.output').addClass("active").text("Пожалуйста, авторизуйтесь").show();
        setTimeout(function () {
            $('.output').removeClass('active').hide();
        }, 3000);
        return;
    }
    $.ajax({
        url: '/weather_data',
        type: 'GET',
        headers: {
            "Authorization": "Bearer " + myToken
        },
        success: function (data) {
            $('.weather-data-table').replaceWith(data);
            $('.output').addClass("active").text("Данные успешно загружены").show();
            $('.data-weather').addClass("active");
            
            setTimeout(function () {
                $('.output').removeClass('active').hide();
            }, 3000);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            $('.output').addClass("active").text("Ошибка загрузки данных").show();
            setTimeout(function () {
                $('.output').removeClass('active').hide();
            }, 3000);
        }
    });
});