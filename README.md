# fullviewapp
Порядок использования

1)Проект выполнен на FastApi.
2)перед получением данных необходимо зарегистрироваться в системе.
3)Для регистрации на сайте необходимо нажать кнопки button с 
текстом "прогноз погоды" "прогноз на завтра"
при нажатии на кнопку, если пользователь не 
авторизован, всплывет модальное окно для прохождения 
регистрации/авторизации в системе.
4)после успешной регистрации и авторизации модальное 
окно сменится окном для ввода данных для запроса прогноза погоды.
5) после заполнения минимальной формы с указанием количества дней и локации,
обновится таблица с данными о погоде на количество дней, указанное при запросе.
6) для получения данных о своих предыдущих запросах необходимо нажать кнопку "мои данные" в шапке сайта.

Порядок установки.

1) при помощи команды git clone [ссылка] или интерактивного меню в используемой IDE склонировать проект.
2) Если на компьютере установлен Docker, то из корневой папки проекта fullviewapp в терминале произвести команду: sudo docker compose build
2.а Если на компьютере не установлен докер, необходимо установить машину ubuntu(для windows) на компьютере согласно инструкциям, потом докер, потом уже в вышеизложенном пункте дальнейшие действия.
3) после того, как произведется сбор образов, в терминале выполнить команду sudo docker compose up -d - запустится проект, просмотреть его можно будет по ссылке в браузере: localhost:5007/

проект синхронизинован с API weatherApi
tested project for Ilya Kalchanka
