from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

db = SQLAlchemy()

# Usuario del blog
class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    favorite_characters = relationship("FavoriteCharacter", back_populates="user")
    favorite_planets = relationship("FavoritePlanet", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

# Planetas
class Planet(db.Model):
    __tablename__ = 'planet'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(100))
    terrain: Mapped[str] = mapped_column(String(100))

    residents = relationship("Person", back_populates="homeworld")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain
        }

# Personajes
class Person(db.Model):
    __tablename__ = 'person'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(20))
    height: Mapped[str] = mapped_column(String(10))
    mass: Mapped[str] = mapped_column(String(10))

    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'))
    homeworld = relationship("Planet", back_populates="residents")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "planet_id": self.planet_id
        }

# Favoritos de personajes
class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_character'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    character_id: Mapped[int] = mapped_column(ForeignKey('person.id'))

    user = relationship("User", back_populates="favorite_characters")
    character = relationship("Person")

# Favoritos de planetas
class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'))

    user = relationship("User", back_populates="favorite_planets")
    planet = relationship("Planet")