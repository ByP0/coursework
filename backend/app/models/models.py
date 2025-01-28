from sqlalchemy import BigInteger, Text, VARCHAR, ForeignKey, Integer, Time, ARRAY, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime, time
from sqlalchemy.dialects.postgresql import UUID
import uuid


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(VARCHAR)
    email: Mapped[str] = mapped_column(VARCHAR, unique=True)
    first_name: Mapped[str] = mapped_column(VARCHAR)
    second_name: Mapped[str] = mapped_column(VARCHAR)
    phone: Mapped[str] = mapped_column(VARCHAR, nullable=True)

class Tickets(Base):
    __tablename__ = 'tickets'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    route: Mapped[str] = mapped_column(VARCHAR, ForeignKey('routes.route'))
    cost: Mapped[int] = mapped_column(Integer)
    start_point: Mapped[str] = mapped_column(VARCHAR)
    end_point: Mapped[str] = mapped_column(VARCHAR)
    departure_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'), nullable=True)

class Routes(Base):
    __tablename__ = 'routes'

    route: Mapped[str] = mapped_column(VARCHAR, primary_key=True)
    points: Mapped[list] = mapped_column(ARRAY)
    minimal_price: Mapped[int] = mapped_column(Integer)
    cost_one_point: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)