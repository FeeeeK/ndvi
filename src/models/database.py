from geoalchemy2 import Geometry, WKBElement  # type: ignore
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class GeoJsonGeometry(Geometry):
    as_binary = "ST_AsGeoJSON"


class Field(Base):  # type: ignore
    __tablename__ = "fields"

    id: int = Column(Integer, primary_key=True, autoincrement=True)  # type: ignore
    geometry: WKBElement = Column(GeoJsonGeometry("POLYGON"))  # type: ignore
