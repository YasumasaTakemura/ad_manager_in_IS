from APIs.db import db
from sqlalchemy.exc import SQLAlchemyError

class DB:
    def insert_no_dup(self,table_data):
        for row in table_data:
            try:
                db.session.add(db.CampaignReport(**row))
                db.session.commit()


            except SQLAlchemyError as e:
                print(e)
                db.session.rollback()
                print('done')
                pass