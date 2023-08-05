class WrongShapeError(ValueError):
    '''
    Generally raised when trying to initialize a ``Qubit`` or ``Gate``
    with an improper shape.
    '''
    pass

class NullVectorError(ValueError):
    '''
    Raised when trying to initialize a ``Qubit`` with the null vector.
    '''
    pass

class NormalizationError(ValueError):
    '''
    Raised when the normalization of a ``Qubit`` is broken.
    '''
    pass

class NonUnitaryInputError(ValueError):
    '''
    Raised when trying to instantiate a ``Gate`` with a nonunitary
    argument.
    '''
    pass

class UndeclaredGateError(NotImplementedError):
    '''
    Raised when the ``qcVirtualMachine`` runs a ``Program`` that calls
    a quantum game before defining it.
    '''
    pass

class UnknownInstruction(NotImplementedError):
    '''
    Catch all exception for malformed instructions which make it
    to the ``qcVirtualMachine``.
    '''
    pass

def _is_power_2(n):
    # Helper function for testing validity of Qubit/Gate sizes

    if not n == int(n):
        return False

    n = int(n)
    if n == 1:
        return True

    elif n >= 2:
        return _is_power_2(n/2.0)

    else:
        return False
