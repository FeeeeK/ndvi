from fastapi import HTTPException

FieldNotFoundError = HTTPException(status_code=404, detail="Field not found")
FieldOverlapError = HTTPException(
    status_code=400, detail="Field overlaps with already existing field"
)
WrongGeometryError = HTTPException(status_code=400, detail="Wrong geometry type, Polygon expected")
