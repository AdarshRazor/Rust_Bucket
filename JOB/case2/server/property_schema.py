from dataclasses import dataclass
from typing import Optional

@dataclass
class Property:
    id: str
    title: str
    price: float
    location: str
    bedrooms: int
    bathrooms: int
    size_sqft: float
    year_built: Optional[int]
    school_rating: Optional[float]
    commute_time: Optional[float]
    has_pool: Optional[bool]
    has_garage: Optional[bool]
    has_garden: Optional[bool]
    image_url: Optional[str] 