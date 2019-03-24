def format_response(status, data=None, error=None, meta=None):
    """
    Стандартный шаблон ответа API сервиса
    :param status - код ответа HTTP
    :param data  - поле с данными ответа
    :param error - поле с описанием ошибки
    :return Объект готовый для передачи через API в нашем формате
    """
    ret = {'success': status, "data": {}}
    if error is not None:
        ret['error'] = error
    if data is not None:
        ret['data'] = data
    if meta is not None:
        ret['meta'] = meta
    return ret
