from typing import Optional
import datetime
from sqlalchemy import DateTime, ForeignKeyConstraint, Index, String, Text, text, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    isActive: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('1'))
    dateCreated: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(60))
    mail: Mapped[Optional[str]] = mapped_column(String(50))
    pass_: Mapped[Optional[str]] = mapped_column('pass', String(150))

    notes: Mapped[list['Notes']] = relationship('Notes', foreign_keys='[Notes.userCreated]', back_populates='user')
    notes_: Mapped[list['Notes']] = relationship('Notes', foreign_keys='[Notes.userUpdated]', back_populates='user_')


class Notes(Base):
    __tablename__ = 'notes'
    __table_args__ = (
        ForeignKeyConstraint(['userCreated'], ['user.id'], name='fk_notes_user'),
        ForeignKeyConstraint(['userUpdated'], ['user.id'], name='fk_notes_user1'),
        Index('fk_notes_user1_idx', 'userUpdated'),
        Index('fk_notes_user_idx', 'userCreated')
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    isActive: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('1'))  # 👈 Integer en lugar de TINYINT
    dateCreated: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    userCreated: Mapped[int] = mapped_column(Integer, nullable=False)
    userUpdated: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(60))
    content: Mapped[Optional[str]] = mapped_column(Text)
    dateUpdated: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    user: Mapped['User'] = relationship('User', foreign_keys=[userCreated], back_populates='notes')
    user_: Mapped['User'] = relationship('User', foreign_keys=[userUpdated], back_populates='notes_')
