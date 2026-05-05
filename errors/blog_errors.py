class BlogErrors(Exception):
    def __init__(self, message: str , status_code: int):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
class CreatingBlogError(BlogErrors):
    def __init__(self):
        super().__init__("SOMETHING WENT WRONG FROM DATABASE SIDE WHILE INSERTING UR BLOG",404)
class NegativeOffsetLimitError(BlogErrors):
    def __init__(self):
        super().__init__("OFFSET AND LIMIT CANNOT BE LESS THAN OR ZERO",404)
class BlogsOutOfRangeError(BlogErrors):
    def __init__(self):
        super().__init___("NO MORE BLOGS TO FETCH",404)
class UpdateError(BlogErrors):
    def __init__(self):
        super().__init__("SOMETHING WENT WRONG IN DATABASES WHILE UPDATING",404)
        

