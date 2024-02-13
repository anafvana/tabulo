from errors.ListPaddingError import ListPaddingError


class InsufficientPaddingError(ListPaddingError):
    def __init__(self):
        self.value = "One or more of the padding values provided is too small."

    def __str__(self):
        return repr(self.value)
