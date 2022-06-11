# ОбщагиНет (@SayNoToHostelBot)

## Тема
Разработка Telegram-бота для добавления, поиска жилья и нахождения соседей с системой подписок.

## Роли
1) Гость;
2) Арендатор;
3) Арендодатель;
4) Администратор.

## Функциональные требования
|       Функционал                  |Готовность|
|:---------------------------------:|:--------:|
|Регистрация арендатора             |    +     |
|Регистрация арендодателя           |    +     |
|Админка                            |    +     |
|Добавление карточки с квартирой    |    -     |
|Просмотр квартир                   |    -     |
|Просмотр квартир (фильтры)         |    -     |
|Подписка на новые квартиры         |    -     |
|Отметка понравившихся квартир      |    -     |
|Получение уведомлений о лайках     |    -     |
|Добавление объявлений о поиске     |    -     |
|Добавление объявлений о товарах    |    -     |
|Подписка на арендодателей          |    -     |
|Выставление оценок арендодателям   |    -     |
|Просмотр информации об арендодателе|    -     |



## Гость
### Регистрация
Пользователь вводит одну из команд: /register_tenant или /register_landlord. В зависимости от этого предлагается ввести данные для регистрации как арендатор и арендодатель соответственно. Для арендатора - полное имя, возраст, пол, город, персональные качества, платежеспособность. Для арендодателя - полное имя, возраст, город.
### Просмотр квартир
Имеет право на просмотр квартир путем вызова команды /get_flats. Бот отправляет список карточек, которые содержат следующую информацию:

- Фотографии
- Владелец
- Стоимость
- Площадь
- Адрес
- Ближайшее метро
- Этаж
- Описание