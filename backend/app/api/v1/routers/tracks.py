from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.database import get_session
from app.schemas import TrackCreate, TrackModel, TrackResponse, MemberModel, ArtistModel
from app.models import Artist, Member, Track

router = APIRouter()


@router.post("/tracks/", response_model=TrackModel)
async def create_track(track: TrackCreate, db: AsyncSession = Depends(get_session)):
    db_track = Track(
        title=track.title,
        artist_id=track.artist_id,
        year=track.year,
        duration=track.duration,
        genre=track.genre
    )
    db.add(db_track)
    await db.commit()
    await db.refresh(db_track)
    
    result = await db.execute(
        select(Artist)
        .where(Artist.id == track.artist_id)
    )
    artist = result.scalars().first()
    
    return TrackModel(
        id=db_track.id,
        title=db_track.title,
        artist_id=db_track.artist_id,
        year=db_track.year,
        duration=db_track.duration,
        genre=db_track.genre,
        artist=ArtistModel(
            id=artist.id,
            name=artist.name,
            country=artist.country,
            formation_year=artist.formation_year,
            disband_year=artist.disband_year,
            awards=artist.awards,
            is_group=artist.is_group,
            members=[]
        )
    )

@router.get("/tracks/", response_model=List[TrackResponse])
async def get_tracks(
    title: Optional[str] = None,
    artist_name: Optional[str] = None,
    genre: Optional[str] = None,
    year_before: Optional[int] = None,
    year_after: Optional[int] = None,
    db: AsyncSession = Depends(get_session)
):
    query = select(
        Track.id,
        Track.title,
        Artist.name.label("artist_name"),
        Track.year,
        Track.duration,
        Track.genre,
        Artist.country,
        Artist.formation_year,
        Artist.disband_year,
        Artist.awards
    ).select_from(Track).join(Artist)
    
    if title:
        query = query.where(Track.title.ilike(f"%{title}%"))
    if artist_name:
        query = query.where(Artist.name.ilike(f"%{artist_name}%"))
    if genre:
        query = query.where(Track.genre.ilike(f"%{genre}%"))
    if year_before:
        query = query.where(Track.year <= year_before)
    if year_after:
        query = query.where(Track.year >= year_after)
    
    result = await db.execute(query)
    tracks = result.all()
    
    response = []
    for track in tracks:
        members_result = await db.execute(
            select(Member)
            .where(Member.artist_id == Artist.id)
            .where(Artist.name == track.artist_name)
        )
        members = members_result.scalars().all()
        
        response.append(TrackResponse(
            id=track.id,
            title=track.title,
            artist=track.artist_name,
            year=track.year,
            duration=track.duration,
            genre=track.genre,
            country=track.country,
            formation_year=track.formation_year,
            disband_year=track.disband_year,
            awards=track.awards,
            members=[
                MemberModel(
                    id=m.id,
                    name=m.name,
                    role=m.role
                )
                for m in members
            ]
        ))
    
    return response

@router.get("/track/{artist_name}/{track_title}", response_model=TrackResponse)
async def get_track_details(artist_name: str, track_title: str, db: AsyncSession = Depends(get_session)):
    track_result = await db.execute(
        select(
            Track.id,
            Track.title,
            Artist.name.label("artist_name"),
            Track.year,
            Track.duration,
            Track.genre,
            Artist.country,
            Artist.formation_year,
            Artist.disband_year,
            Artist.awards
        )
        .select_from(Track)
        .join(Artist)
        .where(
            and_(
                Artist.name == artist_name,
                Track.title == track_title
            )
        )
    )
    track = track_result.first()
    
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    artist_result = await db.execute(
        select(Artist)
        .where(Artist.name == artist_name)
    )
    artist = artist_result.scalars().first()
    
    members = []
    if artist:
        members_result = await db.execute(
            select(Member)
            .where(Member.artist_id == artist.id)
        )
        members = members_result.scalars().all()
    
    return TrackResponse(
        id=track.id,
        title=track.title,
        artist=track.artist_name,
        year=track.year,
        duration=track.duration,
        genre=track.genre,
        country=track.country,
        formation_year=track.formation_year,
        disband_year=track.disband_year,
        awards=track.awards,
        members=[
            MemberModel(
                id=m.id,
                name=m.name,
                role=m.role
            )
            for m in members
        ]
    )

@router.delete("/track/{artist_name}/{track_title}")
async def delete_track(artist_name: str, track_title: str, db: AsyncSession = Depends(get_session)):
    artist_result = await db.execute(
        select(Artist)
        .where(Artist.name == artist_name)
    )
    artist = artist_result.scalars().first()
    
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    track_result = await db.execute(
        select(Track)
        .where(
            and_(
                Track.title == track_title,
                Track.artist_id == artist.id
            )
        )
    )
    track = track_result.scalars().first()
    
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    await db.delete(track)
    await db.commit()
    
    return {"message": "Track deleted successfully"}