from sqlalchemy import Column, ForeignKey, Integer, Text

from .common_base import CommonBase


class Donation(CommonBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
