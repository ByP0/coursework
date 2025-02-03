from sqlalchemy import BigInteger, VARCHAR, TIME, INT, ForeignKey, DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(VARCHAR)
    email: Mapped[str] = mapped_column(VARCHAR, unique=True)
    first_name: Mapped[str] = mapped_column(VARCHAR)
    second_name: Mapped[str] = mapped_column(VARCHAR)
    phone: Mapped[str] = mapped_column(VARCHAR, nullable=True)

class Artists(Base):
    __tablename__ = 'artists'
    artist_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    country: Mapped[str] = mapped_column(VARCHAR(100))
    formation_year: Mapped[date] = mapped_column(DATE, nullable=True)
    breakup_year: Mapped[date] = mapped_column(DATE, nullable=True)
    awards: Mapped[list['Awards']] = relationship("Awards", back_populates="artist")
    members: Mapped[list['Members']] = relationship("Members", back_populates="artist")

class Tracks(Base):
    __tablename__ = 'tracks'
    track_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(VARCHAR(255))
    artist_id: Mapped[int] = mapped_column(ForeignKey('artists.artist_id'))
    release_year: Mapped[date] = mapped_column(DATE)
    duration: Mapped[TIME] = mapped_column(TIME)
    genre_id: Mapped[int] = mapped_column(ForeignKey('genres.genre_id'))
    
    artist: Mapped[Artists] = relationship("Artists", back_populates="tracks")
    genre: Mapped['Genres'] = relationship("Genres", back_populates="tracks")

class Genres(Base):
    __tablename__ = 'genres'
    genre_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    genre_name: Mapped[str] = mapped_column(VARCHAR(100))
    tracks: Mapped[list[Tracks]] = relationship("Tracks", back_populates="genre")

class Members(Base):
    __tablename__ = 'members'
    member_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey('artists.artist_id'))
    full_name: Mapped[str] = mapped_column(VARCHAR(255))
    role: Mapped[str] = mapped_column(VARCHAR(100))

    artist: Mapped[Artists] = relationship("Artists", back_populates="members")

class Awards(Base):
    __tablename__ = 'awards'
    award_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey('artists.artist_id'))
    award_name: Mapped[str] = mapped_column(VARCHAR(255))
    year: Mapped[date] = mapped_column(DATE)

    artist: Mapped[Artists] = relationship("Artists", back_populates="awards")