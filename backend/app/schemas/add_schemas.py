from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Optional
import re

pattern_time = r'^(?:[0-5]\d):[0-5]\d$'

class AddArtist(BaseModel):
    name: Annotated[str, Field(title="Имя группы или артиста")]
    country: Annotated[str, Field(title="Страна")]
    formation_year: Annotated[int, Field(title="Год формирования", ge=1900, lt=2025)]
    breakup_year: Annotated[Optional[int], Field(title="Год распада", default=None, ge=1900, lt=2025)]


class AddTrack(BaseModel):
    title: Annotated[str, Field()]
    artist_id: Annotated[int, Field()]
    release_year: Annotated[int, Field(title="Год релиза", ge=1900, lt=2025)]
    duration: Annotated[str, Field()]
    genre_id: Annotated[int, Field()]

    @model_validator(mode="before")
    def check_model(cls, values):
        duration = values.get("duration")
        if duration:
            if re.match(pattern=pattern_time, string=duration) is None:
                raise ValueError('Invalid time')
        
        return values
    
class AddGenre(BaseModel):
    genre_name: Annotated[str, Field()]


class AddMember(BaseModel):
    artist_id: Annotated[int, Field()]
    full_name: Annotated[str, Field()]
    role: Annotated[str, Field()]


class AddAward(BaseModel):
    artist_id: Annotated[int, Field()]
    award_name: Annotated[str, Field()]
    year: Annotated[int, Field(title="Год вручения награды", ge=1900, lt=2025)]