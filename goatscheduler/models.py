from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from enum import Enum
import os 


Base = declarative_base()


class Components(Base):
    __tablename__ = 'components'
    name = Column(String, primary_key=True)
    component_type = Column(String, nullable=False)
    state = Column(SQLEnum(RunState), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now())



engine = create_engine('sqlite:///goathousing_test2')
print('created engine')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
print('created Session')
session = Session()
print('got session instance')

component = Components(name='goatscheduler')
print(component)
session.add(component)
print('added component')
my_component = session.query(Components).filter_by(name='goatscheduler').first()
print(my_component)
session.commit()
exit(0)


SQLITE = 'sqlite3'


class SchedulerDB:

    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    # Main DB connection ref object
    db_engine = None 
    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print(f'Can not create db engine type {dbtype}')
        
    def create_tables(self):
        metadata = MetaData()
        users = Table(USERS, metadata, 
        Column('id', Integer, primary_key=True),
        Column('first_name', String),
        Column('last_name', String)
        )

        addresses = Table(ADDRESSES, metadata,
        Column('id', Integer, primary_key=True),
        Column('user_id', None, ForeignKey(f'{USERS}.id')),
        Column('email', String, nullable=False),
        Column('address', String)
        )

        try:
            metadata.create_all(self.db_engine)
            print('Tables created')
        except Exception as e:
            print('Error during table creation!')

    # Insert, Update, Delete
    def execute_query(self, query=''):
        if query == '' : return
        print (query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)





SQLITE = 'sqlite3'