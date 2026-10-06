from sqlalchemy import create_engine, Column, Integer, String, Date, Time, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database
DATABASE_URL = "sqlite:///college_events.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# Event table
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    venue = Column(String(200), nullable=False)
    organizer = Column(String(200), nullable=False)
    description = Column(Text, default="")
    capacity = Column(Integer, default=50)


# Registration table
class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True)
    student_name = Column(String(200), nullable=False)
    student_id = Column(String(100), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)


# Create the tables
Base.metadata.create_all(engine)
from sqlalchemy import text

with engine.connect() as conn:
    columns = conn.execute(text("PRAGMA table_info(events)")).fetchall()
    column_names = [column[1] for column in columns]

    if "capacity" not in column_names:
        conn.execute(
            text("ALTER TABLE events ADD COLUMN capacity INTEGER DEFAULT 50")
        )
        conn.commit()