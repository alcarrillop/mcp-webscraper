from pydantic import BaseModel
from typing import Optional, List

class ListingItem(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    price: Optional[str] = None
    bedrooms: Optional[str] = None
    bathrooms: Optional[str] = None
    area: Optional[str] = None
    realtor: Optional[str] = None
    image_url: Optional[str] = None
    link: Optional[str] = None

class ListingResponse(BaseModel):
    listings: List[ListingItem]