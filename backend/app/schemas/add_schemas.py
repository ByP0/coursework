from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Optional
import re
from backend.app.validating_data import country_list, music_awards

pattern_time = r'^(?:[0-5]\d):[0-5]\d$'

class AddArtist(BaseModel):
    name: Annotated[str, Field(title="Имя группы или артиста", examples=["Playboi Carti"])]
    country: Annotated[str, Field(title="Страна", examples=["США"])]
    formation_year: Annotated[int, Field(title="Год формирования", ge=1900, lt=2025, examples=[2019])]
    breakup_year: Annotated[Optional[int], Field(title="Год распада", default=None, ge=1900, lt=2025, examples=[2025])]

    @model_validator(mode="before")
    def check_model(cls, values):
        country = values.get("country")
        if country not in country_list:
            raise ValueError('Invalid country')
        return values


class AddTrack(BaseModel):
    title: Annotated[str, Field(title="Название песни", examples=["RADAR"])]
    artist_id: Annotated[int, Field(title="ID артиста", examples=[1])]
    release_year: Annotated[int, Field(title="Год релиза", ge=1900, lt=2025, examples=[2024])]
    duration: Annotated[str, Field(title="Длительность песни", examples=["2:53"])]
    genre_id: Annotated[int, Field(title="ID жанра", examples=[1])]

    @model_validator(mode="before")
    def check_model(cls, values):
        duration = values.get("duration")
        if duration:
            if re.match(pattern=pattern_time, string=duration) is None:
                raise ValueError('Invalid duration')
        
        return values
    

class AddMember(BaseModel):
    artist_id: Annotated[int, Field(title="ID артиста", examples=[1])]
    full_name: Annotated[str, Field(title="ФИО участника группы", examples=["Джордан Террелл Картер"])]
    role: Annotated[str, Field(title="Роль", examples=["Репер"])]


class AddAward(BaseModel):
    artist_id: Annotated[int, Field(title="ID артиста", examples=[1])]
    award_name: Annotated[str, Field(title="Название награды", examples=["Премия 'Гремми'"])]
    year: Annotated[int, Field(title="Год вручения награды", ge=1900, lt=2025, examples=[2025])]
    
    @model_validator(mode="before")
    def check_model(cls, values):
        award_name = values.get("award_name")
        if award_name not in music_awards:
            raise ValueError('Invalid award name')
        return values