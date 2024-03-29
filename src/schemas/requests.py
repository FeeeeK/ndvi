from geojson_pydantic import FeatureCollection
from pydantic import root_validator

from src.utils.exceptions import WrongGeometryError


class GeoJson(FeatureCollection):
    @root_validator
    def validate_geojson(cls, values):
        if values["features"][0].geometry.type != "Polygon":
            raise WrongGeometryError
        return values


class CreateFieldRequest(GeoJson):
    pass


class FieldGeoJsonRequest(GeoJson):
    pass
