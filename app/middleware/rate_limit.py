from slowapi import Limiter
from slowapi.util import get_remote_address

# Initialize Rate Limiter
limiter = Limiter(key_func=get_remote_address)


def setup_rate_limit(app):
    """Set up rate limiting for the FastAPI application."""
    app.state.limiter = limiter
    from slowapi.errors import RateLimitExceeded
    from slowapi import _rate_limit_exceeded_handler
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)