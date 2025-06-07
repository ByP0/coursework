from pydantic import BaseModel
from typing import List, Optional


class MemberBase(BaseModel):
    name: str
    role: str

class MemberCreate(MemberBase):
    pass

class MemberModel(MemberBase):
    id: int

class ArtistBase(BaseModel):
    name: str
    country: str
    formation_year: Optional[int] = None
    disband_year: Optional[int] = None
    awards: Optional[str] = None
    is_group: bool = False

class ArtistCreate(ArtistBase):
    members: Optional[List[MemberCreate]] = None

class ArtistModel(ArtistBase):
    id: int
    members: List[MemberModel] = []

class TrackBase(BaseModel):
    title: str
    artist_id: int
    year: int
    duration: int
    genre: str

class TrackCreate(TrackBase):
    pass

class TrackModel(TrackBase):
    id: int
    artist: ArtistModel

class TrackResponse(BaseModel):
    id: int
    title: str
    artist: str
    year: int
    duration: int
    genre: str
    country: str
    formation_year: Optional[int]
    disband_year: Optional[int]
    awards: Optional[str]
    members: List[MemberModel] = []