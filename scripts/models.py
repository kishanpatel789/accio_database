from sqlalchemy import (
    Column,
    String,
    Boolean,
    Float,
    Integer,
    DateTime,
    Table,
    ForeignKey,
    func,
    MetaData,
)
from sqlalchemy.orm import mapped_column, relationship, DeclarativeBase
from datetime import datetime, UTC

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime

metadata_obj = MetaData(schema=None)


class Base(DeclarativeBase):
    metadata = metadata_obj


class Book(Base):
    __tablename__ = "book"

    id = mapped_column(String, primary_key=True)
    slug = mapped_column(String, unique=True, nullable=False)
    title = mapped_column(String, unique=True, nullable=False)
    summary = mapped_column(String)
    author = mapped_column(String)
    release_date = mapped_column(DateTime)
    dedication = mapped_column(String)
    pages = mapped_column(Integer)
    cover = mapped_column(String)
    wiki = mapped_column(String)

    chapters = relationship(
        "Chapter",
        lazy="joined",
        order_by="Chapter.order",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Book(id='{self.id}', slug='{self.slug}')>"


class Chapter(Base):
    __tablename__ = "chapter"

    id = mapped_column(String, primary_key=True)
    book_id = mapped_column(ForeignKey("book.id"))
    slug = mapped_column(String, nullable=False)
    order = mapped_column(Integer)
    summary = mapped_column(String)
    title = mapped_column(String, nullable=False)

    def __repr__(self):
        return (
            f"<Chapter(id='{self.id}', book_id='{self.book_id}', slug='{self.slug}')>"
        )


class Character(Base):
    __tablename__ = "character"

    id = mapped_column(String, primary_key=True)
    slug = mapped_column(String, unique=True, nullable=False)
    name = mapped_column(String, nullable=False)
    born = mapped_column(String)
    died = mapped_column(String)
    gender = mapped_column(String)
    species = mapped_column(String)
    height = mapped_column(String)
    weight = mapped_column(String)
    hair_color = mapped_column(String)
    eye_color = mapped_column(String)
    skin_color = mapped_column(String)
    blood_status = mapped_column(String)
    marital_status = mapped_column(String)
    nationality = mapped_column(String)
    animagus = mapped_column(String)
    boggart = mapped_column(String)
    house = mapped_column(String)
    patronus = mapped_column(String)
    image = mapped_column(String)
    wiki = mapped_column(String)

    def __repr__(self):
        return f"<Character(id='{self.id}', slug='{self.slug}')>"


class Movie(Base):
    __tablename__ = "movie"

    id = mapped_column(String, primary_key=True)
    slug = mapped_column(String, unique=True, nullable=False)
    title = mapped_column(String, nullable=False)
    summary = mapped_column(String)
    release_date = mapped_column(DateTime)
    running_time = mapped_column(String)
    budget = mapped_column(String)
    box_office = mapped_column(String)
    rating = mapped_column(String)
    trailer = mapped_column(String)
    poster = mapped_column(String)
    wiki = mapped_column(String)

    def __repr__(self):
        return f"<Movie(id='{self.id}', slug='{self.slug}')>"


class Potion(Base):
    __tablename__ = "potion"

    id = mapped_column(String, primary_key=True)
    slug = mapped_column(String, unique=True, nullable=False)
    name = mapped_column(String, nullable=False)
    effect = mapped_column(String)
    side_effects = mapped_column(String)
    characteristics = mapped_column(String)
    time = mapped_column(String)
    difficulty = mapped_column(String)
    ingredients = mapped_column(String)
    inventors = mapped_column(String)
    manufacturers = mapped_column(String)
    image = mapped_column(String)
    wiki = mapped_column(String)

    def __repr__(self):
        return f"<Potion(id='{self.id}', slug='{self.slug}')>"


class Spell(Base):
    __tablename__ = "spell"

    id = mapped_column(String, primary_key=True)
    slug = mapped_column(String, unique=True, nullable=False)
    name = mapped_column(String, nullable=False)
    incantation = mapped_column(String)
    category = mapped_column(String)
    effect = mapped_column(String)
    light = mapped_column(String)
    hand = mapped_column(String)
    creator = mapped_column(String)
    image = mapped_column(String)
    wiki = mapped_column(String)

    def __repr__(self):
        return f"<Spell(id='{self.id}', slug='{self.slug}')>"
