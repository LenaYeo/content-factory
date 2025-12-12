from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ContentHistory(Base):
    """콘텐츠 생성 히스토리 테이블"""
    __tablename__ = "content_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    business_name = Column(String, nullable=False)
    target_customer = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    tone = Column(String, nullable=False)
    date = Column(String, nullable=False)
    strategy = Column(Text, nullable=True)
    final_content = Column(Text, nullable=False)
    trend_docs = Column(Text, nullable=True)  # JSON string
    best_practice_docs = Column(Text, nullable=True)  # JSON string
