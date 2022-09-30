from sqlalchemy import CheckConstraint, Column, String, Text
from sqlalchemy.orm import declared_attr

from .common_base import CommonBase


class CharityProject(CommonBase):
    @declared_attr
    def __table_args__(cls):
        return (
            *super().__table_args__, CheckConstraint('length(name) > 0'),
            CheckConstraint('length(description) > 0'))

    name = Column(
        String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
