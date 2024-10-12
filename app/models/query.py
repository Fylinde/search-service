from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

class QueryLogModel(BaseModel):
    __tablename__ = 'query_logs'
    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    query = Column(String)
    timestamp = Column(TIMESTAMP)