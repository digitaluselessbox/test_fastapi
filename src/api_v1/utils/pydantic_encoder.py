"""Utility functions for encoding Pydantic models to JSON-compatible formats."""

from fastapi.encoders import jsonable_encoder


def encode_input(data) -> dict:
    """Encode Pydantic model to JSON-compatible dict, excluding None values."""
    data = jsonable_encoder(data)
    data = {k: v for k, v in data.items() if v is not None}
    return data
