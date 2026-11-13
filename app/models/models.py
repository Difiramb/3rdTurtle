from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    region: Mapped[Optional[str]] = mapped_column(String(100))
    logo_url: Mapped[Optional[str]] = mapped_column(String(500))

    players: Mapped[list[Player]] = relationship(back_populates="team")
    home_matches: Mapped[list[Match]] = relationship(
        back_populates="team1", foreign_keys="Match.team1_id"
    )
    away_matches: Mapped[list[Match]] = relationship(
        back_populates="team2", foreign_keys="Match.team2_id"
    )


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    real_name: Mapped[Optional[str]] = mapped_column(String(200))
    role: Mapped[Optional[str]] = mapped_column(String(100))
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("teams.id"))

    team: Mapped[Optional[Team]] = relationship(back_populates="players")
    match_stats: Mapped[list[MatchStat]] = relationship(back_populates="player")


class Hero(Base):
    __tablename__ = "heroes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    role: Mapped[Optional[str]] = mapped_column(String(100))

    match_stats: Mapped[list[MatchStat]] = relationship(back_populates="hero")


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    team1_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)
    team2_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)
    score: Mapped[Optional[str]] = mapped_column(String(20))
    tournament_name: Mapped[str] = mapped_column(String(255), index=True)

    team1: Mapped[Team] = relationship(
        back_populates="home_matches", foreign_keys=[team1_id]
    )
    team2: Mapped[Team] = relationship(
        back_populates="away_matches", foreign_keys=[team2_id]
    )
    stats: Mapped[list[MatchStat]] = relationship(
        back_populates="match", cascade="all, delete-orphan"
    )


class MatchStat(Base):
    __tablename__ = "match_stats"
    __table_args__ = (
        UniqueConstraint("match_id", "player_id", "hero_id", name="uq_match_stats_entry"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), index=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), index=True)
    hero_id: Mapped[int] = mapped_column(ForeignKey("heroes.id"), index=True)
    kills: Mapped[int] = mapped_column(Integer, default=0)
    deaths: Mapped[int] = mapped_column(Integer, default=0)
    assists: Mapped[int] = mapped_column(Integer, default=0)

    match: Mapped[Match] = relationship(back_populates="stats")
    player: Mapped[Player] = relationship(back_populates="match_stats")
    hero: Mapped[Hero] = relationship(back_populates="match_stats")
