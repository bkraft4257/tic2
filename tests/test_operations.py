from tic_core import operations


def test_force_input_to_list_int_scalar():
    """ 
    """
    result = operations.force_type_to_list(1)
    assert [1] == result


def test_force_input_to_list_int_list():
    """
    """
    result = operations.force_type_to_list([1, 2, 3])
    assert [1,2,3] == result


def test_force_input_to_list_str_scalar():
    """
    """
    result = operations.force_type_to_list('hello')
    assert ['hello'] == result


def test_force_input_to_list_str_scalar_mismatch():
    """
    """
    result = operations.force_type_to_list('hello')
    assert ['hello'] == result


def test_force_input_to_list_str_list():
    """
    """
    result = operations.force_type_to_list(['hello','world'])
    assert ['hello','world'] == result
