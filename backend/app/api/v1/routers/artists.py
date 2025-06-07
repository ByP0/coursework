from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_session
from app.schemas import ArtistCreate, ArtistModel
from app.models import Artist, Member


router = APIRouter(prefix='/artists')


@router.post("/", response_model=ArtistModel)
async def create_artist(artist: ArtistCreate, db: AsyncSession = Depends(get_session)):
    db_artist = Artist(
        name=artist.name,
        country=artist.country,
        formation_year=artist.formation_year,
        disband_year=artist.disband_year,
        awards=artist.awards,
        is_group=artist.is_group
    )
    db.add(db_artist)
    await db.commit()
    await db.refresh(db_artist)

    if artist.members:
        for member in artist.members:
            db_member = Member(
                artist_id=db_artist.id,
                name=member.name,
                role=member.role
            )
            db.add(db_member)
        await db.commit()
    
    result = await db.execute(
        select(Artist)
        .where(Artist.id == db_artist.id)
        .options(selectinload(Artist.members)) 
    )
    db_artist = result.scalars().first()
    
    members = []
    if db_artist.members:
        members = [
            {
                "id": m.id,
                "name": m.name,
                "role": m.role
            }
            for m in db_artist.members
        ]
    
    return {
        "id": db_artist.id,
        "name": db_artist.name,
        "country": db_artist.country,
        "formation_year": db_artist.formation_year,
        "disband_year": db_artist.disband_year,
        "awards": db_artist.awards,
        "is_group": db_artist.is_group,
        "members": members
    }