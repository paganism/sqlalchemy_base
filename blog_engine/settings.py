from models import Base
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session


engine = sqlalchemy.create_engine('sqlite:///blog.db', echo=False) # echo - debug mode
Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
