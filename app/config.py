import os
from functools import lru_cache

@lru_cache()
def get_environment() -> str:
    """Get the current environment (development or production)."""
    return os.getenv("ENVIRONMENT", "production").lower()

def is_development() -> bool:
    """Check if the current environment is development."""
    return get_environment() == "development"

def is_production() -> bool:
    """Check if the current environment is production."""
    return get_environment() == "production"
