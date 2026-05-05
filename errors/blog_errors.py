class BlogErrors(Exception):
    def __init__(self, message: str , status_code):
        super().__init__(*args)