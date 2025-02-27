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
            console.log(data)
        //     if (dataString.response.error) {
        //         $('.output').addClass("active");
        //         $('.output').text(dataString.response.error).show();
        //         $('#register-form')[0].reset();

        //     } else if (dataString.response.text) {
        //         $('.output').addClass("active");
        //         $('.output').text(dataString.response.text).show();
        //         $('#register-form')[0].reset();
        //     }
        //     setTimeout(function () {
        //         $('.output').removeClass('active');
        //     }, 3000);
        // },
        // error: function (jqXHR, textStatus, errorThrown) {
        //     // Обработка ошибок AJAX-запроса
        //     $('.output').text('An error occurred: ' + textStatus).show();
        //     setTimeout(function () {
        //         $('.output').removeClass('active').hide();
        //     }, 3000);
        }
    });
});