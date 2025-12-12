import json
from datetime import datetime
from database.model import ContentHistory
from database.session import db_session
from typing import List, Optional


class ContentRepository:
    """콘텐츠 히스토리 저장소"""
    
    def save(
        self,
        business_name: str,
        target_customer: str,
        channel: str,
        tone: str,
        strategy: str,
        final_content: str,
        trend_docs: List[str] = None,
        best_practice_docs: List[str] = None
    ) -> int:
        """
        콘텐츠 생성 결과 저장
        
        Returns:
            생성된 레코드의 ID
        """
        session = db_session.get_session()
        
        try:
            content = ContentHistory(
                business_name=business_name,
                target_customer=target_customer,
                channel=channel,
                tone=tone,
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                strategy=strategy,
                final_content=final_content,
                trend_docs=json.dumps(trend_docs or [], ensure_ascii=False),
                best_practice_docs=json.dumps(best_practice_docs or [], ensure_ascii=False)
            )
            
            session.add(content)
            session.commit()
            
            content_id = content.id
            return content_id
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_all(self, limit: int = 50) -> List[ContentHistory]:
        """
        모든 히스토리 조회 (최신순)
        
        Args:
            limit: 조회 개수 제한
            
        Returns:
            히스토리 목록
        """
        session = db_session.get_session()
        
        try:
            histories = session.query(ContentHistory)\
                .order_by(ContentHistory.id.desc())\
                .limit(limit)\
                .all()
            return histories
        finally:
            session.close()
    
    def get_by_id(self, content_id: int) -> Optional[ContentHistory]:
        """
        ID로 히스토리 조회
        
        Args:
            content_id: 콘텐츠 ID
            
        Returns:
            히스토리 또는 None
        """
        session = db_session.get_session()
        
        try:
            content = session.query(ContentHistory)\
                .filter(ContentHistory.id == content_id)\
                .first()
            return content
        finally:
            session.close()
    
    def search_by_business(self, business_name: str) -> List[ContentHistory]:
        """
        비즈니스명으로 검색
        
        Args:
            business_name: 비즈니스명
            
        Returns:
            히스토리 목록
        """
        session = db_session.get_session()
        
        try:
            histories = session.query(ContentHistory)\
                .filter(ContentHistory.business_name.like(f"%{business_name}%"))\
                .order_by(ContentHistory.id.desc())\
                .all()
            return histories
        finally:
            session.close()
    
    def delete(self, content_id: int) -> bool:
        """
        히스토리 삭제
        
        Args:
            content_id: 콘텐츠 ID
            
        Returns:
            삭제 성공 여부
        """
        session = db_session.get_session()
        
        try:
            content = session.query(ContentHistory)\
                .filter(ContentHistory.id == content_id)\
                .first()
            
            if content:
                session.delete(content)
                session.commit()
                return True
            return False
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


# 전역 인스턴스
content_repository = ContentRepository()
