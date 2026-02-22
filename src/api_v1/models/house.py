"""bnb house model"""

from typing import List
from beanie import Document
from pydantic import BaseModel, ConfigDict


class Review(Document):
    review: str


class House(Document):
    """House model"""

    house_id: int
    title: str
    city: str
    image_path: str
    guestCapacity: int
    wifi: bool
    laundry: bool
    reviews: List[str] = []

    class Settings:
        name = "houses"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "house_id": 1,
                "title": "Your beautiful vacation home",
                "city": "Best city ever",
                "image_path": "somewhere.png",
                "guestCapacity": 4,
                "wifi": True,
                "laundry": False,
                "review": "Excellent house!",
            }
        }
    )


class UpdateHouse(BaseModel):
    title: str | None = None
    city: str | None = None
    image_path: str | None = None
    guestCapacity: int | None = None
    wifi: bool | None = None
    laundry: bool | None = None

    class Settings:
        name = "house"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Your beautiful vacation home",
                "city": "Best city ever",
                "image_path": "somewhere.png",
                "guestCapacity": 4,
                "wifi": True,
                "laundry": False,
            }
        }
    )
