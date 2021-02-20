#from goatscheduler.goatscheduler.Component import Component
from typing import ContextManager
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import func
from contextlib import contextmanager
from .RunState import RunState
from . import logger
import os 


Base = declarative_base()

class Components(Base):
    __tablename__ = 'components'
    name = Column(String, primary_key=True)
    component_type = Column(String, nullable=False)
    state = Column(SQLEnum(RunState), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now())
    # dependencies = relationship('Dependencies', primaryjoin='dependencies.component_name==components.name')
    # dependents = relationship('Dependents', primaryjoin='dependents.component_name==components.name')

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
    component_name = Column(String, ForeignKey('components.name'), nullable=False)
    dependency_name = Column(String, ForeignKey('components.name'), nullable=False)

class Dependents(Base):
    __tablename__ = 'dependents'
    id = Column(Integer, primary_key=True)
    component_name = Column(String, ForeignKey('components.name'), nullable=False)
    dependent_name = Column(String, ForeignKey('components.name'), nullable=False)

class SchedulerBackend:

    def __init__(
        self, 
        scheduler_name: str, 
        reset_backend: bool = False
    ):
        sqlite_path = os.path.expanduser('~/.goatscheduler')
        sqlite_db_path = os.path.join(sqlite_path, f'{scheduler_name}.sqlitedb')

        if not os.path.exists(sqlite_path):
            os.makedirs(sqlite_path)

        if os.path.exists(sqlite_db_path) and reset_backend:
            logger.log(20, f'Resetting database for schedule {scheduler_name}')
            os.remove(sqlite_db_path)

        engine_path = f'sqlite:///{sqlite_db_path}'
        engine = create_engine(engine_path, connect_args={"check_same_thread": False})
        logger.log(20, f'Creating DB tables if they don\'t already exist')
        Base.metadata.create_all(engine)

        self.Session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False))

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            logger.log(40, f'Exception in session_scope')
            raise Exception 
        finally: 
            session.close()


    def get_component(self, name: str) -> Components:
        with self.session_scope() as session:
            return session.query(Components).filter_by(name=name).first()

    def get_component_state(self, name: str) -> RunState:
        return self.get_component(name=name).state

    def add_component(
        self,
        name: str, 
        component_type: str, 
        state: RunState=RunState.NONE
    ):
        if component_type != 'task' and component_type != 'schedule':
            print(f'Component is not type task or schedule. type: {component_type}')
            raise Exception

        if self.get_component(name=name) is None:
            component = Components(
                name=name,
                component_type=component_type,
                state=state
            )
            logger.log(20, f'Component with name {name} created')
            with self.session_scope() as session:
                session.add(component)
        else:
            logger.log(40, f'Component with name {name} already exists')
            raise Exception

    def add_component_dependency(
        self,
        component_name: str, 
        dependency_name: str
    ):
        dependency = Dependencies(component_name=component_name, dependency_name=dependency_name)
        with self.session_scope() as session:
            session.add(dependency)
        logger.log(20, f'Added dependency {dependency_name} to component {component_name}')

    def add_component_dependent(
        self,
        component_name: str,
        dependent_name: str
    ):
        dependent = Dependents(component_name=component_name, dependent_name=dependent_name)
        with self.session_scope() as session:
            session.add(dependent)
        logger.log(20, f'Added dependent {dependent_name} to component {component_name}')

    def update_component_state(self, name: str, state: RunState):
        with self.session_scope() as session:
            component = session.query(Components).filter_by(name=name).first()
            if not component:
                raise Exception 
            component.state = state


