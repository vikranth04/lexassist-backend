from fastapi import Header, HTTPException


def verify_api_key(x_api_key: str = Header(None)):
    """
    Placeholder for future authentication support.
    For now, it allows all requests but provides the signature for API key verification.
    """
    if x_api_key:
        # Future logic: check key validity
        pass
    return x_api_key
