from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Optional
import re

pattern_time = r'^(?:[01]\d|2[0-3]):[0-5]\d$'

class AddArtist(BaseModel):
    name: Annotated[str, Field(title="Имя группы или артиста")]
    country: Annotated[str, Field(title="Страна")]
    formation_year: Annotated[str, Field(title="Год формирования")]
    breakup_year: Annotated[Optional[str], Field(title="Год распада",default=None)]


class AddTrack(BaseModel):
    title: Annotated[str, Field()]
    artist_id: Annotated[int, Field()]
    release_year: Annotated[str, Field()]
    duration: Annotated[str, Field()]
    genre_id: Annotated[int, Field()]

    @model_validator(mode="before")
    def check_model(cls, values):
        duration = values.get("duration")
        if duration:
            if re.match(pattern=pattern_time, string=duration) is None:
                raise ValueError('Invalid time')
        
        return values