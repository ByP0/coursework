from sqlalchemy import BigInteger, VARCHAR, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship


Base = declarative_base()


class Artists(Base):
    __tablename__ = 'artists'

    artist_name: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    country: Mapped[str] = mapped_column(VARCHAR(100))
    
    tracks: Mapped[list['Tracks']] = relationship("Tracks", back_populates="artist")
    awards: Mapped[list['Awards']] = relationship("Awards", back_populates="artist")


class Groups(Base):
    __tablename__ = 'groups'

    group_name: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    country: Mapped[str] = mapped_column(VARCHAR(100))
    formation_year: Mapped[int] = mapped_column(nullable=True)
    breakup_year: Mapped[int] = mapped_column(nullable=True)
    
    tracks: Mapped[list['Tracks']] = relationship("Tracks", back_populates="group")
    awards: Mapped[list['Awards']] = relationship("Awards", back_populates="group")
    members: Mapped[list['Members']] = relationship("Members", back_populates="group")


class Tracks(Base):
    __tablename__ = 'tracks'
    
    track_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    artist_name: Mapped[str] = mapped_column(ForeignKey('artists.artist_name'), nullable=True)
    group_name: Mapped[str] = mapped_column(ForeignKey('groups.group_name'), nullable=True)
    release_year: Mapped[int] = mapped_column(nullable=False)
    duration: Mapped[str] = mapped_column(nullable=False)
    genre_name: Mapped[str] = mapped_column(ForeignKey('genres.genre_name'), nullable=False)
    
    artist: Mapped['Artists'] = relationship("Artists", back_populates="tracks")
    genre: Mapped['Genres'] = relationship("Genres", back_populates="tracks")
    group: Mapped['Groups'] = relationship("Groups", back_populates="tracks")


class Genres(Base):
    __tablename__ = 'genres'

    genre_name: Mapped[str] = mapped_column(VARCHAR(100), primary_key=True)
    tracks: Mapped[list['Tracks']] = relationship("Tracks", back_populates="genre")


class Members(Base):
    __tablename__ = 'members'
    
    member_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(ForeignKey('groups.group_name'))
    full_name: Mapped[str] = mapped_column(VARCHAR(255))
    role: Mapped[str] = mapped_column(VARCHAR(100))

    group: Mapped['Groups'] = relationship("Groups", back_populates="members")


class Awards(Base):
    __tablename__ = 'awards'

    award_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    award_name: Mapped[str] = mapped_column(VARCHAR(255))
    year: Mapped[int] = mapped_column()
    artist_name: Mapped[str] = mapped_column(ForeignKey('artists.artist_name'), nullable=True)
    group_name: Mapped[str] = mapped_column(ForeignKey('groups.group_name'), nullable=True)

    artist: Mapped['Artists'] = relationship("Artists", back_populates="awards")
    group: Mapped['Groups'] = relationship("Groups", back_populates="awards")
