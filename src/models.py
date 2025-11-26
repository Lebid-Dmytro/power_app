from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    countries = relationship("Country", back_populates="region", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Region(id={self.id}, name='{self.name}')"


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    population = Column(BigInteger, nullable=False)

    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    region = relationship("Region", back_populates="countries")

    def __repr__(self):
        return f"Country(name='{self.name}', population={self.population})"
