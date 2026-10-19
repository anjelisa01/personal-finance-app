
from sqlalchemy.orm import Session


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db
