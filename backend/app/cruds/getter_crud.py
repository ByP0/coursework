from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from backend.app.models.models import Artists, Genres, Tracks, Awards, Members
from backend.app.schemas.getter_schemas import GetArtist


async def get_all_group_songs(session: AsyncSession, artist_id: int):
    stmt = select(Tracks).where(Tracks.artist_id == artist_id)
    result = await session.execute(stmt)
    songs = result.scalars().all()
    return songs

async def get_all_songs(session: AsyncSession):
    stmt = select(Tracks)
    result = await session.execute(stmt)
    songs = result.scalars().all()
    return list(songs)


async def get_all_group(session: AsyncSession) -> list[GetArtist]:
    stmt_1 = select(Artists)
    result_artists: Result = await session.execute(stmt_1)
    artists = result_artists.scalars().all()

    artists_ids = [arists.artist_id for arists in artists]
    stmt_2 = select(Tracks).where(Tracks.artist_id.in_(artists_ids))
    result_tracks = await session.execute(stmt_2)
    tracks = result_tracks.scalars().all()
    tracks_dict = {}

    for track in tracks:
        if track.artist_id not in tracks_dict:
            tracks_dict[track.artist_id] = []
        tracks_dict[track.artist_id].append(
            {
                "track_id": track.track_id,
                "title": track.title,
                "release_year": track.release_year,
                "duration": track.duration,
                "genre_id": track.genre_id,
            }
        )
    
    stmt_3 = select(Members).where(Members.artist_id.in_(artists_ids))
    result_members = await session.execute(stmt_3)
    members = result_members.scalars().all()
    members_dict = {}

    for member in members:
        if member.artist_id not in members_dict:
            members_dict[member.artist_id] = []
        members_dict[member.artist_id].append(
            {
                "member_id": member.member_id,
                "full_name": member.full_name,
                "role": member.role
            }
        )

    stmt_4 = select(Awards).where(Awards.artist_id.in_(artists_ids))
    result_awards = await session.execute(stmt_4)
    awards = result_awards.scalars().all()
    awards_dict = {}

    for award in awards:
        if award.artist_id not in awards_dict:
            awards_dict[award.artist_id] = []
        awards_dict[award.artist_id].append(
            {
                "award_id": award.award_id,
                "award_name": award.award_name,
                "year": award.year
            }
        )

    
    artists_data = [
        GetArtist(
            artist_id=artist.artist_id,
            name=artist.name,
            country=artist.country,
            formation_year=artist.formation_year,
            breakup_year=artist.breakup_year,
            tracks=tracks_dict.get(artist.artist_id, []),
            members=members_dict.get(artist.artist_id, []),
            awards=awards_dict.get(artist.artist_id, [])
        ) 
        for artist in artists
    ]
    return artists_data

async def get_all_genres(session: AsyncSession):
    stmt = select(Genres)
    result = await session.execute(stmt)
    genres = result.scalars().all()
    return genres

async def get_group_by_id(session: AsyncSession, artist_id: int):
    stmt = select(Artists).where(Artists.artist_id == artist_id)
    result = await session.execute(stmt)
    group = result.scalar_one_or_none()
    return group

async def get_all_awards(session: AsyncSession):
    stmt = select(Awards)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_award_by_artist_id(session: AsyncSession, artist_id: int):
    stmt = select(Awards).where(Awards.artist_id == artist_id)
    result = await session.execute(stmt)
    return result.scalars().all()