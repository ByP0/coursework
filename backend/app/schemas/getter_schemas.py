from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, List

class GetArtist(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    artist_id: int
    name: str
    country: str
    formation_year: int
    breakup_year: int
    tracks: Annotated[list[dict], Field(default=None, examples=[[
        {
            "track_id": 1,
            "title": "RADAR",
            "release_year": 2025,
            "duration": "2:53",
            "genre_id": 1,
        }
        ]])]
    members: Annotated[list[dict], Field(default=None, examples=[[
        {
            "member_id": 1,
            "full_name": "Джордан Террелл Картер",
            "role": "Репер"
        }
        ]])]
    awards: Annotated[list[dict], Field(default=None, examples=[[
        {
            "award_id": 1,
            "award_name": "Грэмми",
            "year": 2025,
        }
        ]])]