from app.exceptions import SvsException


class svsApiResponse():
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


@parametrized
def svs_exceptions(fn, bugsnag=None):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except SvsException as ex:
            return svsApiResponse(status=False, error=ex.message, code=ex.result_code)
        except Exception as ex:
            # Тут должен быть вызов bugsnag для прода
            # Чтото вроде:
            # err_string = "Something went wrong"
            # if bugsnag is not None:
            #    bugsnag.notify(ex)
            # else:
            err_string = str(ex)
            return svsApiResponse(status=False, error=err_string, code=500)

    return wrapper


def api_response(fn):
    def wrapper(*args, **kwargs):
        response = fn(*args, **kwargs)

        try:
            return response().response()
        except:
            print(1)
    return wrapper
