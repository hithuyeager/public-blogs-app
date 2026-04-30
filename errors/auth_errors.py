class AuthError(Exception):
    def __init__(self,message: str,status_code: int):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class ExpiredTokenError(AuthError):
    def __init__(self):
        super().__init__("TOKEN EXPIRED",400)
class InvalidTokenError(AuthError):
    def __init__(self):
        super().__init__("INVALID TOKEN",400)
class InvalidTokenTypeError(AuthError):
    def __init__(self):
        super().__init__("WRONG TOKEN TYPE",400)
class UserALreadyExistError(AuthError):
    def __init__(self):
        super().__init__("USER ALREADY EXIST",404)
class UserNotExistError(AuthError):
    def __init__(self):
        super().__init__("USER DOES NOT EXIST",404)
class WrongPasswordError(AuthError):
    def __init__(self):
        super().__init__("WRONG PASSWORD",400)
class TokenStolenError(AuthError):
    def __init__(self):
        super().__init__("USING STOLEN TOKEN AFTER USER LOGOUT",400)


