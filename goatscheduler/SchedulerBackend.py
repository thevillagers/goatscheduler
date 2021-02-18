from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
from .RunState import RunState
import os 


Base = declarative_base()

class Components(Base):
    __tablename__ = 'components'
    name = Column(String, primary_key=True)
    component_type = Column(String, nullable=False)
    state = Column(SQLEnum(RunState), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now())
    dependencies = relationship('Dependencies', primaryjoin='Dependencies.component_name==Components.name')
    dependents = relationship('Dependents', primaryjoin='Dependents.component_name==Components.name')

class ComponentStateHistory(Base):
    __tablename__ = 'component_state_history'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    component_type = Column(String, nullable=False)
    state = Column(SQLEnum(RunState), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)

class Dependencies(Base):
    __tablename__ = 'dependencies'
    id = Column(Integer, primary_key=True)
    component_name = Column(String, ForeignKey('Components.name'), nullable=False)
    dependency_name = Column(String, ForeignKey('Components.name'), nullable=False)

class Dependents(Base):
    __tablename__ = 'dependents'
    id = Column(Integer, primary_key=True)
    component_name = Column(String, ForeignKey('Components.name'), nullable=False)
    dependent_name = Column(String, ForeignKey('Components.name'), nullable=False)

class SchedulerBackend:

    def __init__(
        self, 
        scheduler_name: str, 
        reset_db: bool = False
    ):
        sqlite_path = os.path.expanduser('~/.goatscheduler')
        sqlite_db_path = os.path.join(sqlite_path, 'goatscheduler.sqlitedb')

        if not os.path.exists(sqlite_path):
            os.makedirs(sqlite_path)

        if os.path.exists(sqlite_db_path) and reset_db:
            os.remove(sqlite_db_path)

        engine_path = f'sqlite:///{sqlite_db_path}'
        engine = create_engine(engine_path)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)

        self.session = Session()

    def get_component(self, name: str) -> Components:
        return self.session.query(Components).filter_by(name=name).first()

    def add_component(
        self,
        name: str, 
        component_type: str, 
        state: RunState=RunState.NONE
    ):
        if component_type != 'task' and component_type != 'schedule':
            raise Exception

        if self.get_component(name=name) is not None:
            component = Components(
                name=name,
                component_type=component_type,
                state=state
            )
            self.session.add(component)
            self.session.commit()
        else:
            raise Exception

    def add_component_dependency(
        self,
        component_name: str, 
        dependency_name: str
    ):


    def update_component_state(self, name: str, state: RunState):
        component = self.get_component(name=name)
        if not component:
            raise Exception 
        
        component.state = state 
        self.session.commit()
