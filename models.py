from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Website(Base):
    __tablename__ = 'websites'

    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    created = Column(DateTime)

    scan = relationship("Scan", uselist=False, back_populates="website")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(320))
    password = Column(String(60))
    first_name = Column(String(255))
    last_name = Column(String(255))
    credit_amount = Column(Integer)
    role = Column(Integer)
    created = Column(DateTime)

    websites = relationship("Website", backref="user")

class Scan(Base):
    __tablename__ = 'scans'

    id = Column(Integer, primary_key=True)
    website_id = Column(Integer, ForeignKey('websites.id'))
    status = Column(Integer)
    created_date = Column(DateTime)
    started_date = Column(DateTime)
    finished_date = Column(DateTime)

    website = relationship("Website", back_populates="scan")
    scan_data = relationship("ScanData", backref="scan")


class ScanData(Base):
    __tablename__ = 'scan_data'

    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey('scans.id'))
    key = Column(String(255))
    value = Column(String(255))