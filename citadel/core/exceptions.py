class DomainException(Exception):
    """Base exception for all domain errors."""
    pass

class InvalidStateTransitionError(DomainException):
    """Raised when an invalid state transition is attempted."""
    pass

class PanicValueError(DomainException):
    """Raised when a value is outside panic limits."""
    pass

class UnauthorizedRoleError(DomainException):
    """Raised when a user role is not authorized for an action."""
    pass

class EntityNotFoundError(DomainException):
    """Raised when an entity is not found."""
    pass

class ValidationError(DomainException):
    """Raised when domain validation fails."""
    pass
