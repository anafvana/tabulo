from errors.ListPaddingError import ListPaddingError


class NotAMatrixError(ListPaddingError):
    def __init__(self, value=None):
        if not value:
            self.value = "The list provided is not a matrix."
            return
        
        self.value = value

    def __str__(self):
        return repr(self.value)
