from typing import List, Optional

from geoalchemy2 import func  # type: ignore
from geojson_pydantic import Polygon
from sqlalchemy import delete, insert, select

from src.models.database import Field
from src.schemas.responses import FieldResponse
from src.utils import SessionManager


class FieldRepository:
    @staticmethod
    async def get_all(limit: int = 100, offset: int = 0) -> List[FieldResponse]:
        query = select(Field).limit(limit).offset(offset)
        async with SessionManager() as session:
            fields: List[Field] = (await session.execute(query)).scalars().all()

        return [FieldResponse(id=field.id, geometry=field.geometry.data) for field in fields]

    @staticmethod
    async def get_by_id(id: int) -> Optional[FieldResponse]:
        query = select(Field).where(Field.id == id)
        async with SessionManager() as session:
            field: Optional[Field] = (await session.execute(query)).scalars().first()

        if field:
            return FieldResponse(id=field.id, geometry=field.geometry.data)
        return None

    @staticmethod
    async def get_by_geometry(geometry: Polygon) -> Optional[FieldResponse]:
        query = select(Field).where(Field.geometry.ST_Intersects(geometry.wkt))
        async with SessionManager() as session:
            field: Optional[Field] = (await session.execute(query)).scalars().first()
        if field:
            return FieldResponse(id=field.id, geometry=field.geometry.data)
        return None

    @staticmethod
    async def create(geometry: Polygon) -> Optional[FieldResponse]:
        intersects_select = select(Field).where(
            Field.geometry.ST_Intersects(func.ST_GeomFromText(geometry.wkt))
        )
        query = (
            insert(Field).values(geometry=func.ST_GeomFromText(geometry.wkt)).returning(Field.id)
        )
        # Insert only if geometry not overlaps with any other geometry
        async with SessionManager() as session:
            is_intersects = (await session.execute(intersects_select)).scalars().first()  # type: ignore
            if is_intersects:
                return None
            field_id: int = (await session.execute(query)).scalars().first()  # type: ignore

        return FieldResponse(id=field_id, geometry=geometry)

    @staticmethod
    async def delete(id: int) -> Optional[FieldResponse]:
        query = delete(Field).where(Field.id == id).returning(Field.id, Field.geometry)
        async with SessionManager() as session:
            deleted = (await session.execute(query)).one_or_none()
        return FieldResponse(id=id, geometry=deleted[1].data) if deleted else None
