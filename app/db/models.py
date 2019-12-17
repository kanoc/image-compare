from datetime import datetime
from typing import List

from app.db import db


class Image(db.Model):  # type: ignore
    """Holds data about an uploaded image."""

    __tablename__ = 'images'

    id: int = db.Column(db.Integer, primary_key=True)
    filename: str = db.Column(db.String(256), nullable=False)
    date_uploaded: datetime = db.Column(db.DateTime(), nullable=False)
    feature_vector: List[float] = db.Column(db.ARRAY(db.Float))
