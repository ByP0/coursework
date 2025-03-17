from pydantic import BaseModel

class GetArtist(BaseModel):
    artist_id: int
    name: str
    country: str
    formation_year: int
    breakup_year: int