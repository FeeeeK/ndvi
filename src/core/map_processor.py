from datetime import datetime, timedelta
from io import BytesIO
from typing import IO, Optional

import ee  # type: ignore
import httplib2  # type: ignore
from geojson_pydantic import Polygon

from src.config import GEE_CREDENTIALS_PATH, GEE_SERVICE_EMAIL, NDVI_PALETTE
from src.utils import _async


class MapProcessor:
    def __init__(self):
        self.credentials = ee.ServiceAccountCredentials(GEE_SERVICE_EMAIL, GEE_CREDENTIALS_PATH)
        ee.Initialize(self.credentials)

    @_async
    def get_field_image(
        self,
        geometry: Polygon,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = datetime.now(),
    ) -> str:
        if date_from is None:
            date_from = datetime.now() - timedelta(days=90)
        if date_to is None:
            date_to = datetime.now()
        area = ee.Geometry.Polygon(geometry.coordinates)
        image = self._get_image(area, date_from, date_to)
        rgb_image = image.visualize(min=0, max=3000, bands=["B4", "B3", "B2"])
        return self._get_thumbnail(rgb_image, area)

    @_async
    def get_ndvi_image(
        self,
        geometry: Polygon,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> str:
        if date_from is None:
            date_from = datetime.now() - timedelta(days=90)
        if date_to is None:
            date_to = datetime.now()
        area = ee.Geometry.Polygon(geometry.coordinates)
        image = self._get_image(area, date_from, date_to)
        ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
        ndvi_image = ndvi.visualize(min=-0.5, max=1, palette=NDVI_PALETTE)
        return self._get_thumbnail(ndvi_image, area)

    @_async
    def download_image(self, url: str) -> IO[bytes]:
        # I know about aiohttp, but I don't want to add another dependency just for this
        http = httplib2.Http()
        content = http.request(url)[1]
        fp = BytesIO(content)
        fp.seek(0)
        return fp

    def _get_image(
        self,
        area: ee.Geometry,
        date_from: datetime,
        date_to: Optional[datetime] = None,
    ) -> ee.Image:
        return (
            ee.ImageCollection("COPERNICUS/S2_SR")
            .filterDate(date_from, date_to)
            .filterMetadata("CLOUD_COVERAGE_ASSESSMENT", "less_than", 10)
            .filterBounds(area)
            .map(lambda image: self._mask_clouds(image).clip(area))
        ).median()

    def _mask_clouds(self, image: ee.Image) -> ee.Image:
        QA60: ee.Image = image.select(["QA60"])
        clouds = QA60.bitwiseAnd(1 << 10).Or(QA60.bitwiseAnd(1 << 11))
        return image.updateMask(clouds.Not())

    def _get_thumbnail(self, image: ee.Image, area: ee.Geometry) -> str:
        return image.getThumbURL(params={"format": "png", "dimensions": "1000", "region": area})
