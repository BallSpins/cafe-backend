from src.database import Base, engine
from src.models import *

def migrate():
    print('Dropping existing tables (if any)...')
    Base.metadata.drop_all(bind=engine)

    print('Migrating database...')
    Base.metadata.create_all(bind=engine)
    print('Done!')

if __name__ == '__main__':
    migrate()