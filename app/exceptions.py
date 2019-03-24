class SvsException(BaseException):
    """Исключение для передачи кодов ошибок и описаний клиенту"""
    result_code = 500
    message = "unknown"

    def __init__(self, result_code, message):
        self.result_code = result_code
        self.message = message
