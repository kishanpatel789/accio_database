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

    alias_names = relationship(
        "CharacterAliasNames",
        lazy="joined",
        cascade="all, delete-orphan",
    )
    family_members = relationship(
        "CharacterFamilyMembers",
        lazy="joined",
        cascade="all, delete-orphan",
    )
    jobs = relationship(
        "CharacterJobs",
        lazy="joined",
        cascade="all, delete-orphan",
    )
    romances = relationship(
        "CharacterRomances",
        lazy="joined",
        cascade="all, delete-orphan",
    )
    titles = relationship(
        "CharacterTitles",
        lazy="joined",
        cascade="all, delete-orphan",
    )
    wands = relationship(
        "CharacterWands",
        lazy="joined",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Character(id='{self.id}', slug='{self.slug}')>"


class CharacterAliasNames(Base):
    __tablename__ = "character_alias_names"

    character_id = mapped_column(ForeignKey("character.id"), primary_key=True)
    alias_names = mapped_column(String, primary_key=True)

    def __repr__(self):
        return f"<CharacterAliasNames(character_id='{self.character_id}', alias_names='{self.alias_names}')>"


class CharacterFamilyMembers(Base):
    __tablename__ = "character_family_members"

    character_id = mapped_column(ForeignKey("character.id"), primary_key=True)
    family_members = mapped_column(String, primary_key=True)

    def __repr__(self):
        return f"<CharacterFamilyMembers(character_id='{self.character_id}', family_members='{self.family_members}')>"


class CharacterJobs(Base):
    __tablename__ = "character_jobs"

    character_id = mapped_column(ForeignKey("character.id"), primary_key=True)
    jobs = mapped_column(String, primary_key=True)

    def __repr__(self):
        return (
            f"<CharacterJobs(character_id='{self.character_id}', jobs='{self.jobs}')>"
        )


class CharacterRomances(Base):
    __tablename__ = "character_romances"

    character_id = mapped_column(ForeignKey("character.id"), primary_key=True)
    romances = mapped_column(String, primary_key=True)

    def __repr__(self):
        return f"<CharacterRomances(character_id='{self.character_id}', romances='{self.romances}')>"


class CharacterTitles(Base):
    __tablename__ = "character_titles"

    character_id = mapped_column(ForeignKey("character.id"), primary_key=True)
    titles = mapped_column(String, primary_key=True)

    def __repr__(self):
        return f"<CharacterTitles(character_id='{self.character_id}', titles='{self.titles}')>"


class CharacterWands(Base):
    __tablename__ = "character_wands"

    character_id = mapped_column(ForeignKey("character.id"), primary_key=True)
    wands = mapped_column(String, primary_key=True)

    def __repr__(self):
        return f"<CharacterWands(character_id='{self.character_id}', wands='{self.wands}')>"


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

    directors = relationship(
        "MovieDirectors",
        lazy="joined",
        cascade="all, delete-orphan",
    )
    screenwriters = relationship(
        "MovieScreenwriters",
        lazy="joined",
        cascade="all, delete-orphan",
    )
    producers = relationship(
        "MovieProducers",
        lazy="joined",
        cascade="all, delete-orphan",
    )
    cinematographers = relationship(
        "MovieCinematographers",
        lazy="joined",
        cascade="all, delete-orphan",
    )
    editors = relationship(
        "MovieEditors",
        lazy="joined",
        cascade="all, delete-orphan",
    )
    distributors = relationship(
        "MovieDistributors",
        lazy="joined",
        cascade="all, delete-orphan",
    )
    music_composers = relationship(
        "MovieMusicComposers",
        lazy="joined",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Movie(id='{self.id}', slug='{self.slug}')>"


class MovieDirectors(Base):
    __tablename__ = "movie_directors"

    movie_id = mapped_column(ForeignKey("movie.id"), primary_key=True)
    directors = mapped_column(String, primary_key=True)

    def __repr__(self):
        return f"<MovieDirectors(movie_id='{self.movie_id}', directors='{self.directors}')>"


class MovieScreenwriters(Base):
    __tablename__ = "movie_screenwriters"

    movie_id = mapped_column(ForeignKey("movie.id"), primary_key=True)
    screenwriters = mapped_column(String, primary_key=True)

    def __repr__(self):
        return f"<MovieScreenwriters(movie_id='{self.movie_id}', screenwriters='{self.screenwriters}')>"


class MovieProducers(Base):
    __tablename__ = "movie_producers"

    movie_id = mapped_column(ForeignKey("movie.id"), primary_key=True)
    producers = mapped_column(String, primary_key=True)

    def __repr__(self):
        return f"<MovieProducers(movie_id='{self.movie_id}', producers='{self.producers}')>"


class MovieCinematographers(Base):
    __tablename__ = "movie_cinematographers"

    movie_id = mapped_column(ForeignKey("movie.id"), primary_key=True)
    cinematographers = mapped_column(String, primary_key=True)

    def __repr__(self):
        return f"<MovieDirectors(movie_id='{self.movie_id}', cinematographers='{self.cinematographers}')>"


class MovieEditors(Base):
    __tablename__ = "movie_editors"

    movie_id = mapped_column(ForeignKey("movie.id"), primary_key=True)
    editors = mapped_column(String, primary_key=True)

    def __repr__(self):
        return f"<MovieEditors(movie_id='{self.movie_id}', editors='{self.editors}')>"


class MovieDistributors(Base):
    __tablename__ = "movie_distributors"

    movie_id = mapped_column(ForeignKey("movie.id"), primary_key=True)
    distributors = mapped_column(String, primary_key=True)

    def __repr__(self):
        return f"<MovieDistributors(movie_id='{self.movie_id}', distributors='{self.distributors}')>"


class MovieMusicComposers(Base):
    __tablename__ = "movie_music_composers"

    movie_id = mapped_column(ForeignKey("movie.id"), primary_key=True)
    music_composers = mapped_column(String, primary_key=True)

    def __repr__(self):
        return f"<MovieMusicComposers(movie_id='{self.movie_id}', music_composers='{self.music_composers}')>"


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
