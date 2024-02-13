from typing import Iterable, List, Mapping, Sequence, Sized, Type, cast
from errors.IncorrectPaddingError import IncorrectPaddingError
from errors.InsufficientPaddingError import InsufficientPaddingError
from errors.NotAMatrixError import NotAMatrixError


def is_matrix(matrix: Sequence[Sized], accept_str_row: bool = False) -> bool:
    """
    Check if sequence contains only equal-length elements.
    Criteria:
    1. Is a sequence (list, tuple, array)
    2. Is not a string
    3. The child elements are sized (list, tuple, set, string [if accept_str_row is True])
    4. All child elements have the same size

    :param matrix: A sequence containing Sized elements. Example: list[list[str]]
    :param accept_str_matrix: Whether a string can constitute a row of the matrix. Default is False
    :return: True if child elements are of same length, false otherwise
    """

    # Any single string is a sequence of size=1 strings. Exclude from the concept of matrix    
    if isinstance(matrix, str):
        return False

    try:
        # Ensure Sequence type by indexing
        template = matrix[0]

        # Exclude matrices with string children if accept_str_row is not set
        if not accept_str_row and any(isinstance(row, str) for row in matrix):
            return False

        # Filter out elements in list with length different from first element. Return whether True for empty list, False otherwise
        return not [x for x in matrix if len(x) != len(template)]
    except:
        return False


def calculate_max_length(matrix: Sequence[Sequence], accept_str_row: bool = False) -> list[int]:
    """
    Calculate maximum length of each column of a matrix

    :param matrix: A sequence parent (matrix) containing n equal-sized sequences (rows). Example: list[list[str]]
    :param accept_str_matrix: Whether a string can constitute a row of the matrix. Default is False
    :return: True if child elements are of same length, false otherwise
    """
    if not is_matrix(matrix, accept_str_row):
        raise NotAMatrixError
    
    # Return array with the length of the longest cell for each of the columns
    return [max([len(str(row[col])) for row in matrix]) for col in range(len(matrix[0]))]


def pad(matrix: Iterable, header: bool = False, lengths: list[int] | None = None) -> list[list[str]]:
    # Cast matrix to list, if necessary
    if not isinstance(matrix, list):
        matrix_type: Type[Iterable] = type(matrix)

        try:
            if isinstance(matrix, Mapping):
                raise NotAMatrixError(f"Cannot pad data of type {matrix_type} without data loss")
            
            matrix = list(matrix)
        except (TypeError, ValueError) as e:
            raise NotAMatrixError(f"Iterable of type {matrix_type} cannot be cast to list") from e
        
    # Make matrix rows iterable (list), if necessary 
    row_type = type(matrix[0])
    if not all(isinstance(row, row_type) for row in matrix): # Element 0 still checked against itself to avoid out of bounds in single-item matrices
        raise NotAMatrixError(f"Alleged matrix contains rows of different types.")
    
    if not issubclass(row_type, Iterable):
        row_keys = max([row.__dict__.keys() for row in matrix], key=len)
        if not row_keys:
            raise NotAMatrixError(f"Alleged matrix does not contain iterable rows.")

        matrix = [[getattr(row, k) for k in row_keys] for row in matrix]
        if header:
            matrix = [list(row_keys)] + matrix

    min_padding = calculate_max_length(matrix)

    if lengths:
        if len(lengths) != len(matrix[0]):
            raise IncorrectPaddingError

        paddings_too_small = [x for x, y in zip(lengths, min_padding) if x < y]
        if paddings_too_small:
            raise InsufficientPaddingError

    else:
        lengths = min_padding

    padded_matrix: List[List[str]] = [[str(cell) + (" " * (padding - len(cell))) for cell, padding in zip(row, lengths)] for row in matrix]
    if matrix_type:
        try:
            padded_matrix = cast(matrix_type, padded_matrix)
        except (TypeError, ValueError) as e:
            pass  # types not compatible
        except KeyError as e:
            pass  # No matching key in dict
        
    return padded_matrix

def print_table(matrix:Iterable):
    if not is_matrix(matrix):
        matrix = pad(matrix)

    for row in matrix:
        print(f"| {' | '.join(row)} |")
