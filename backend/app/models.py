from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    country = Column(String(50), nullable=False)
    formation_year = Column(Integer)
    disband_year = Column(Integer)
    awards = Column(String)
    is_group = Column(Boolean, default=False)

    tracks = relationship("Track", back_populates="artist")
    members = relationship("Member", back_populates="artist", cascade="all, delete")

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)

    artist = relationship("Artist", back_populates="members")

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id", ondelete="CASCADE"))
    year = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    genre = Column(String(50), nullable=False)

    artist = relationship("Artist", back_populates="tracks")