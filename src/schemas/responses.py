from geojson_pydantic import Polygon
from pydantic import BaseModel


class FieldResponse(BaseModel):
    id: int
    geometry: Polygon
