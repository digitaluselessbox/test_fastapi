from typing import List, Annotated
from fastapi import APIRouter, HTTPException, status, Path


from models.house import House, UpdateHouse
from utils import pydantic_encoder

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=House)
async def create_house(house: House):
    await house.insert()
    return house


@router.get("/", response_model=List[House])
async def get_houses():
    houses = await House.find_all().to_list()
    return houses


# house_id: Annotated[int, Path(
#     title="The ID of the house",        # OpenAPI title (im JSON, nicht sichtbar in UI)
#     description="Must be between 0-1000", # erscheint in Swagger UI als Beschreibung
#     ge=0,             # greater or equal (minimum)
#     le=1000,          # less or equal (maximum)
#     gt=0,             # greater than (exclusiveMinimum)
#     lt=1000,          # less than (exclusiveMaximum)
#     alias="id",       # anderer Name im Request
#     deprecated=True,  # als veraltet markieren in Swagger
#     example=42,       # Beispielwert in Swagger UI
# )]


@router.get("/{house_id}", response_model=House)
async def get_house(
    house_id: Annotated[
        int,
        Path(
            title="The ID of the house.",
            description="Must be between 0-1000",
            ge=0,
            le=1000,
            example=42,
        ),
    ],
):
    """get a house by its custom house_id"""

    house = await House.find_one({"house_id": house_id})
    if not house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"House with house_id {house_id} not found",
        )

    return house


@router.put("/{house_id}", response_model=House)
async def update_house(house_id: int, house_data: UpdateHouse):
    """update a house by its custom house_id"""

    house = await House.find_one({"house_id": house_id})
    if not house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"House with house_id {house_id} not found",
        )

    encoded_house_data = pydantic_encoder.encode_input(house_data)
    await house.update({"$set": encoded_house_data})

    updated_house = await House.find_one({"house_id": house_id})
    return updated_house


@router.delete("/{house_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_house(house_id: int):
    """delete a house by its custom house_id"""

    house = await House.find_one({"house_id": house_id})
    if not house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"House with house_id {house_id} not found",
        )
    await house.delete()
    return {"message": "House deleted successfully"}


@router.post("/{house_id}/reviews", response_model=House)
async def add_review(house_id: int, review: str):
    """add a review to a house identified by custom house_id"""

    house = await House.find_one({"house_id": house_id})
    if not house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"House with house_id {house_id} not found",
        )
    await house.update({"$push": {"reviews": review}})
    updated_house = await House.find_one({"house_id": house_id})
    return updated_house


# Example of how to use MongoDB ObjectId for lookup instead of custom house_id:
#
# from beanie import PydanticObjectId
#
# @router.get("/{id}", response_model=House)
# async def get_house(id: PydanticObjectId):
#     """ get a house by its MongoDB object_id """
#     house = await House.get(id)
#     if not house:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"House with id {id} not found",
#         )

#     return house
