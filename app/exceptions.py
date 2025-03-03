from typing import Dict


class CustomAPIError(Exception):
    def __init__(self, message: str, status_code: int, details: Dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


def validation_error(field: str, reason: str) -> CustomAPIError:
    """Validation error for invalid inputs."""
    return CustomAPIError(
        message=f"Invalid input for {field}: {reason}",
        status_code=400,
        details={"field": field, "reason": reason}
    )


def not_found_error(resource: str, identifier: str) -> CustomAPIError:
    """Resource not found error."""
    return CustomAPIError(
        message=f"{resource} with identifier {identifier} not found",
        status_code=404,
        details={"resource": resource, "identifier": identifier}
    )


def auth_error(message: str) -> CustomAPIError:
    """Authentication error."""
    return CustomAPIError(
        message=f"Authentication error: {message}",
        status_code=401,
        details={}
    )


def server_error(message: str) -> CustomAPIError:
    """Internal server error."""
    return CustomAPIError(
        message=f"Server error: {message}",
        status_code=500,
        details={}
    )


def handle_validation_error(field: str, value: str) -> CustomAPIError:
    return CustomAPIError(f"Invalid {field}: {value}", 400)


def handle_not_found_error(resource: str, identifier: str) -> CustomAPIError:
    return CustomAPIError(f"{resource} with ID {identifier} not found", 404)


def handle_auth_error(message: str) -> CustomAPIError:
    return CustomAPIError(message, 401)


def handle_server_error(message: str) -> CustomAPIError:
    return CustomAPIError(f"Server error: {message}", 500)