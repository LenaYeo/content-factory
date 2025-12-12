from typing import Dict, List, TypedDict, Optional


class AgentType:
    """에이전트 타입 상수"""
    STRATEGY = "STRATEGY_AGENT"
    CONTENT = "CONTENT_AGENT"
    REVIEW = "REVIEW_AGENT"

    @classmethod
    def to_korean(cls, role: str) -> str:
        """에이전트 역할을 한글로 변환"""
        if role == cls.STRATEGY:
            return "전략 수립"
        elif role == cls.CONTENT:
            return "콘텐츠 생성"
        elif role == cls.REVIEW:
            return "검토 및 최적화"
        else:
            return role


class ContentState(TypedDict):
    """콘텐츠 생성 워크플로우 전체 상태"""
    # 사용자 입력
    business_name: str
    business_features: str
    target_customer: str
    channel: str  # blog, instagram, email
    tone: str
    
    # Agent 처리 과정
    messages: List[Dict]  # Agent들의 대화 기록
    strategy: Optional[str]  # 전략 수립 결과
    draft_content: Optional[str]  # 초안 콘텐츠
    final_content: Optional[str]  # 최종 콘텐츠
    
    # RAG 관련
    trend_docs: List[str]  # 검색된 트렌드 문서
    best_practice_docs: List[str]  # 검색된 모범 사례 문서
    
    # 상태 추적
    prev_node: str
