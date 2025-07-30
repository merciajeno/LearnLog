from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from main import db
from datetime import date

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)


    subjects: Mapped[list["Subject"]] = relationship(back_populates="user")

    xp = mapped_column(Integer, default=0)
    streak = mapped_column(Integer, default=0)
    last_logged = mapped_column(String, nullable=True)



class Subject(db.Model):
    __tablename__ = 'subject'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)

    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'))
    user: Mapped["User"] = relationship(back_populates="subjects")

    logs: Mapped[list["Log"]] = relationship(back_populates="subject")


class Log(db.Model):
    __tablename__ = 'log'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(default=date.today)

    subject_id: Mapped[int] = mapped_column(db.ForeignKey("subject.id"))
    subject: Mapped["Subject"] = relationship(back_populates="logs")
    was_revised: Mapped[bool] = mapped_column(Boolean,default=False)
    log_type: Mapped[str] = mapped_column(String,default='learning')