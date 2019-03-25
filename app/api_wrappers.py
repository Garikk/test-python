from app.exceptions import SvsException


class svsApiResponse():
    """
    Класс стандартного формата ответа сервиса
    """
    def __init__(self, status=True, data=None, meta=None, error=None, code=200, hide_data_if_none=False):
        self.status = status
        self.data = data
        self.meta = meta
        self.error = error
        self.code = code
        self.hide_data_if_none = hide_data_if_none

    def response(self):
        ret = {'success': self.status}
        if not self.hide_data_if_none:
            ret["data"] = {}
        if self.error is not None:
            ret['error'] = self.error
        if self.data is not None:
            ret['data'] = self.data
        if self.meta is not None:
            ret['meta'] = self.meta
        return ret, self.code


def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


def svs_exceptions(fn):
    """
    Декоратор для ресурсов который при возникновении ошибок не обрушивает сераис, а возвращает минимальный комментарий
    также отсюда хорощо вызывать bugsnag
    :param fn:
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except SvsException as ex:
            return svsApiResponse(status=False, error=ex.message, code=ex.result_code)
        except Exception as ex:
            return svsApiResponse(status=False, error=ex, code=500)

    return wrapper


def api_response(fn):
    """
    Декоратор оформления ответа ресурсов в формате flask-restful
    :param fn:
    :return:
    """

    def wrapper(*args, **kwargs):
        response = fn(*args, **kwargs)

        if isinstance(response, svsApiResponse):
            return response.response()
        else:
            return response().response()

    return wrapper
