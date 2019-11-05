
def connection_checker(function):
    """
    Returns function when connection with Hive is setted up.
    """

    def function_wrapper(self, *args):
        if self.connection_status() is not None:
            print("Connection stable!")
            return function(self, *args)
        else:
            print("Operation invalid! Check your database connection!")

    return function_wrapper
