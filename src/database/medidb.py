from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sshtunnel import SSHTunnelForwarder

import settings

server = SSHTunnelForwarder(
    (settings.DATABASES['server']['HOST']),
    ssh_username=settings.DATABASES['server']['USER'],
    ssh_password=settings.DATABASES['server']['PASS'],
    remote_bind_address=(settings.DATABASES['server']['BIND_ADDRESS'], int(settings.DATABASES['server']['BIND_PORT'])))

server.start()

SQLALCHEMY_DATABASE = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(user=settings.DATABASES['mysql']['USER'],
                                                                                password=settings.DATABASES['mysql']['PASS'],
                                                                                host=server.local_bind_host,
                                                                                port=server.local_bind_port,
                                                                                db=settings.DATABASES['mysql']['DATABASE'])

engine = create_engine(SQLALCHEMY_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()