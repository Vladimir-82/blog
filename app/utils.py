class Message:
    """Class for messages to user"""
    unauthorized = (
        'Только зарегистрированные пользователи могу использовать '
        'сервис. Пройдите регистрацию или авторизацию.'
    )
    success_register = 'Вы успешно зарегистрировались'
    error_register = 'Ошибка регистрации'
    link_already_exist = 'Ссылка уже сокращалась Вами!'
    does_not_have_list = 'У вас пока что нет записей!'