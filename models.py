from database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean
from sqlalchemy.orm import relationship


class Scan(Base):
    __tablename__ = 'scans'

    id = Column(Integer, primary_key=True)
    website_id = Column(Integer, ForeignKey('websites.id'))
    status = Column(Integer)
    created_date = Column(DateTime)
    started_date = Column(DateTime)
    finished_date = Column(DateTime)

    website = relationship("Website", back_populates="scans")
    tests = relationship("Test", uselist=False, back_populates="scan")


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey('scans.id'))
    name = Column(String(50))
    status = Column(Integer)
    started_date = Column(DateTime)
    finished_date = Column(DateTime)

    scan = relationship("Scan", back_populates="tests")
    test_data = relationship("TestData", backref="test")


class TestData(Base):
    __tablename__ = 'test_data'

    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey('tests.id'))
    key = Column(String(255))
    value = Column(String(255))
    data_type = Column(Integer)


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


class Website(Base):
    __tablename__ = 'websites'

    id = Column(Integer, primary_key=True)
    protocol = Column(String(5))
    hostname = Column(String(64))
    verified = Column(Boolean(1))
    user_id = Column(Integer, ForeignKey('users.id'))
    created = Column(DateTime)

    scans = relationship("Scan", uselist=False, back_populates="website")

    def get_url(self):
        return (self.protocol + "://" + self.hostname)
