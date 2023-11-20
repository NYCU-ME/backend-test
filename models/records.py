from sqlalchemy.orm import sessionmaker
from datetime import datetime

from . import db


class Records:
    def __init__(self, sql_engine):
        Session = sessionmaker(bind=sql_engine)
        self.session = Session()

    def get_record(self, record_id):
        return self.session.query(db.Record).filter_by(id=record_id, status=1).first()
    
    def get_records(self, domain_id):
        return self.session.query(db.Record).filter_by(domain_id=domain_id, status=1).all()
	
    def add_record(self, domain_id, record_type, value, ttl):
        now = datetime.now()
        regDate = now
        record = db.Record(domain_id=domain_id, 
                        type=record_type, 
                        value=value, 
                        ttl=ttl, 
                        regDate=regDate, 
                        status=1)
        self.session.add(record)
        self.session.commit()

    def del_record(self, record_id):
        records = self.session.query(db.Record).filter_by(id=record_id).all()
        now = datetime.now()
        expDate = now
        for record in records:
            record.status = 0
            record.expDate = now
        self.session.commit()
