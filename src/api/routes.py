from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.core import MapProcessor
from src.repositories import FieldRepository
from src.schemas.requests import CreateFieldRequest, FieldGeoJsonRequest
from src.schemas.responses import FieldResponse
from src.utils.exceptions import FieldNotFoundError, FieldOverlapError

router = APIRouter(prefix="/api")
map_processor = MapProcessor()


@router.get(
    "/field",
    response_model=FieldResponse,
    responses={404: {"description": "Field not found"}},
)
async def get_field_by_id(field_id: int):
    """Get field by id"""
    field = await FieldRepository.get_by_id(field_id)
    if field is None:
        raise FieldNotFoundError
    return field


@router.post(
    "/field",
    response_model=FieldResponse,
    responses={404: {"description": "Field not found"}},
)
async def get_field_by_geojson(request: FieldGeoJsonRequest):
    """Get field by geojson"""
    geometry = request.features[0].geometry
    field = await FieldRepository.get_by_geometry(geometry)
    if field is None:
        raise FieldNotFoundError
    return field


@router.post(
    "/create_field",
    response_model=FieldResponse,
    responses={400: {"description": "Field overlaps with already existing field"}},
)
async def create_field(request: CreateFieldRequest):
    """Create a new field, returns 400 if field overlaps with already existing one"""
    geometry = request.features[0].geometry
    field = await FieldRepository.create(geometry)
    if field is None:
        raise FieldOverlapError
    return field


@router.delete(
    "/field",
    response_model=FieldResponse,
    responses={404: {"description": "Field not found"}},
)
async def delete_field(field_id: int):
    deleted_field = await FieldRepository.delete(field_id)
    if deleted_field is None:
        raise FieldNotFoundError
    return deleted_field


@router.get(
    "/image",
    response_class=StreamingResponse,
    responses={404: {"description": "Field not found"}},
)
async def get_image(field_id: int):
    """Get image of field"""
    field = await FieldRepository.get_by_id(field_id)
    if field is None:
        raise FieldNotFoundError
    image_url = await map_processor.get_field_image(field.geometry)
    image = await map_processor.download_image(image_url)
    return StreamingResponse(image, media_type="image/png")


@router.get("/ndvi", response_class=StreamingResponse)
async def get_ndvi(field_id: int):
    """Get NDVI image of field"""
    field = await FieldRepository.get_by_id(field_id)
    if field is None:
        raise FieldNotFoundError
    image_url = await map_processor.get_ndvi_image(field.geometry)
    image = await map_processor.download_image(image_url)
    return StreamingResponse(image, media_type="image/png")
