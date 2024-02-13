from errors.ListPaddingError import ListPaddingError


class IncorrectPaddingError(ListPaddingError):
    def __init__(self):
        self.value = (
            "The list of paddings provided does not match the shape of the matrix."
        )

    def __str__(self):
        return repr(self.value)
