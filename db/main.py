from sqlalchemy import *
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
 
# Define the MySQL engine using MySQL Connector/Python
engine = sqlalchemy.create_engine(
    'mysql+mysqlconnector://root:root123@localhost:3306/CanchasAlquiler',
    echo=True)
 
# Define and create the table
Base = declarative_base()
class User(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'Usuario'

    id =     Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nombre = Column(String(length=60), nullable=False, unique=False)
    clave =  Column(String(length=100), nullable=False, unique=False)
    correo = Column(String(length=100), nullable=False, unique=False)
    apodo =  Column(String(length=50), nullable=False, unique=False)
    tipo_usuario = Column(Integer, nullable=False, unique=False)
    telefono = Column(String(length=100), nullable=False, unique=False)
    numero_reservas = Column(Integer, nullable=True, unique=False)
 
    def __repr__(self):
        return "<User(name='{0}', fullname='{1}', nickname='{2}')>".format(
                            self.nombre, self.correo, self.clave)
 
Base.metadata.create_all(engine)
 
# Create a session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()
 
# Add a user
jwk_user = User(nombre='jesper', clave='JesperWisborgKrogh@asd.co', correo="sa@sd.com", apodo='&#x1f42c;',tipo_usuario=1,telefono="0",numero_reservas=3212)
session.add(jwk_user)
session.commit()
 
# Query the user
our_user = session.query(User).filter_by(nombre='jesper').first()
print('\nOur User:')
print(our_user)
