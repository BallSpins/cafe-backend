import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.utils import DATABASE_URL, ADMIN_TOKEN
print(DATABASE_URL,ADMIN_TOKEN)

if not DATABASE_URL:
    raise ValueError('DATABASE_URL environment variable is not set.')

engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()