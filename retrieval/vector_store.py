import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from typing import List, Optional
from utils.config import get_embeddings
import os


# 벡터 스토어 저장 경로
CHROMA_PERSIST_DIR = "./data/chroma_db"


@st.cache_resource
def initialize_vector_stores():
    """마케팅 트렌드와 모범 사례 벡터 스토어 초기화"""
    
    # 디렉토리 생성
    os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
    
    embeddings = get_embeddings()
    
    # 1. 마케팅 트렌드 데이터
    trend_documents = _create_trend_documents()
    trend_store = Chroma.from_documents(
        documents=trend_documents,
        embedding=embeddings,
        collection_name="marketing_trends",
        persist_directory=f"{CHROMA_PERSIST_DIR}/trends"
    )
    
    # 2. 채널별 모범 사례 데이터
    best_practice_documents = _create_best_practice_documents()
    practice_store = Chroma.from_documents(
        documents=best_practice_documents,
        embedding=embeddings,
        collection_name="best_practices",
        persist_directory=f"{CHROMA_PERSIST_DIR}/practices"
    )
    
    return trend_store, practice_store


def _create_trend_documents() -> List[Document]:
    """마케팅 트렌드 문서 생성"""
    trends = [
        {
            "content": """
            2024-2025 마케팅 트렌드: 개인화와 AI 활용
            
            소규모 비즈니스에서 AI를 활용한 개인화 마케팅이 필수가 되었습니다. 
            고객 데이터를 기반으로 맞춤형 메시지를 전달하는 것이 핵심입니다.
            특히 소셜 미디어에서는 짧고 강렬한 메시지가 효과적이며,
            스토리텔링을 통한 감성적 연결이 중요합니다.
            """,
            "metadata": {"source": "Marketing Trends 2024", "category": "personalization"}
        },
        {
            "content": """
            콘텐츠 마케팅의 핵심: 가치 제공과 신뢰 구축
            
            현대 소비자들은 단순한 광고보다 가치 있는 정보를 원합니다.
            교육적이고 유용한 콘텐츠를 제공하여 신뢰를 쌓는 것이 중요합니다.
            블로그, 이메일, SNS 모든 채널에서 일관된 메시지와 톤을 유지하며,
            고객의 문제를 해결하는 솔루션을 제시해야 합니다.
            """,
            "metadata": {"source": "Content Marketing Guide", "category": "value"}
        },
        {
            "content": """
            소셜 미디어 마케팅: 짧고 강렬한 메시지
            
            인스타그램, 페이스북 등 SNS에서는 3초 내에 주목을 끌어야 합니다.
            강렬한 첫 문장, 시각적 요소, 그리고 명확한 CTA(Call To Action)가 필수입니다.
            해시태그는 5-10개 정도가 적당하며, 타겟 고객층이 많이 사용하는 태그를 선택해야 합니다.
            스토리 기능을 활용한 짧은 영상이나 이미지 시리즈도 효과적입니다.
            """,
            "metadata": {"source": "Social Media Marketing 2024", "category": "social"}
        },
        {
            "content": """
            이메일 마케팅의 황금률: 제목과 개인화
            
            이메일 제목은 40자 이내로 작성하며, 긴급성이나 호기심을 자극해야 합니다.
            수신자의 이름을 포함하고, 과거 구매 이력이나 관심사를 반영한 개인화 메시지가 열람률을 2-3배 높입니다.
            본문은 간결하게 핵심만 전달하고, 모바일에서도 읽기 쉽게 짧은 단락으로 구성합니다.
            명확한 CTA 버튼 하나만 배치하여 전환율을 극대화하세요.
            """,
            "metadata": {"source": "Email Marketing Best Practices", "category": "email"}
        },
        {
            "content": """
            블로그 SEO 최적화: 검색 엔진 친화적 글쓰기
            
            블로그 글은 최소 800자 이상 작성하며, 제목에 주요 키워드를 포함합니다.
            소제목(H2, H3)을 활용하여 구조화하고, 각 섹션마다 핵심 키워드를 자연스럽게 배치합니다.
            첫 단락에서 독자의 문제를 제시하고, 중간에 해결책을, 마지막에 행동 촉구를 배치하는 구조가 효과적입니다.
            내부 링크와 외부 권위 있는 소스로의 링크를 포함하여 SEO 점수를 높입니다.
            """,
            "metadata": {"source": "Blog SEO Guide 2024", "category": "blog"}
        }
    ]
    
    return [
        Document(page_content=trend["content"], metadata=trend["metadata"])
        for trend in trends
    ]


def _create_best_practice_documents() -> List[Document]:
    """채널별 모범 사례 문서 생성"""
    practices = [
        {
            "content": """
            인스타그램 캡션 모범 사례:
            
            ✨ [강렬한 첫 문장으로 시작]
            [제품/서비스가 해결하는 문제 제시]
            
            [구체적인 혜택 2-3가지]
            • 혜택 1
            • 혜택 2
            • 혜택 3
            
            [감성적 연결 문구]
            
            [명확한 행동 촉구]
            
            #관련해시태그1 #관련해시태그2 #관련해시태그3
            """,
            "metadata": {"channel": "instagram", "type": "caption"}
        },
        {
            "content": """
            블로그 포스트 모범 사례:
            
            제목: [숫자나 질문 형식으로 호기심 유발]
            
            도입부:
            - 독자가 겪는 문제 공감하기
            - 이 글에서 얻을 수 있는 것 명시
            
            본문:
            1. [첫 번째 핵심 포인트]
               - 구체적인 설명과 예시
            
            2. [두 번째 핵심 포인트]
               - 실전 적용 방법
            
            3. [세 번째 핵심 포인트]
               - 주의사항과 팁
            
            결론:
            - 핵심 내용 요약
            - 다음 단계 제시 (CTA)
            """,
            "metadata": {"channel": "blog", "type": "structure"}
        },
        {
            "content": """
            이메일 마케팅 모범 사례:
            
            제목: [긴급성/호기심/혜택 중 하나 강조, 40자 이내]
            
            안녕하세요 [이름]님,
            
            [개인화된 인사 및 관심사 언급]
            
            [핵심 메시지: 제안하는 가치]
            
            [구체적인 혜택 3가지 bullet points]
            • 혜택 1
            • 혜택 2
            • 혜택 3
            
            [명확한 CTA 버튼]
            → [행동 유도 문구]
            
            [추신: 긴급성이나 추가 혜택 언급]
            """,
            "metadata": {"channel": "email", "type": "template"}
        },
        {
            "content": """
            성공적인 카피라이팅 공식:
            
            AIDA 공식:
            A (Attention): 주목 - 강렬한 첫 문장
            I (Interest): 관심 - 독자의 문제와 연결
            D (Desire): 욕구 - 솔루션 제시와 혜택 강조
            A (Action): 행동 - 명확한 CTA
            
            감성 공략 포인트:
            - 두려움(FOMO): "놓치면 후회할" 요소
            - 소속감: "우리는 ~한 사람들입니다"
            - 성취감: "당신도 할 수 있습니다"
            
            구체성의 힘:
            - 추상적: "빠른 배송" 
            - 구체적: "주문 후 24시간 내 배송"
            """,
            "metadata": {"channel": "general", "type": "copywriting"}
        }
    ]
    
    return [
        Document(page_content=practice["content"], metadata=practice["metadata"])
        for practice in practices
    ]


def search_marketing_trends(query: str, k: int = 2) -> List[Document]:
    """마케팅 트렌드 검색"""
    trend_store, _ = initialize_vector_stores()
    try:
        return trend_store.similarity_search(query, k=k)
    except Exception as e:
        st.error(f"트렌드 검색 중 오류: {str(e)}")
        return []


def search_best_practices(channel: str, k: int = 2) -> List[Document]:
    """채널별 모범 사례 검색"""
    _, practice_store = initialize_vector_stores()
    query = f"{channel} 마케팅 모범 사례 콘텐츠 구조"
    try:
        # 채널별 필터링
        results = practice_store.similarity_search(query, k=k)
        # 해당 채널 또는 일반(general) 문서만 필터링
        filtered = [
            doc for doc in results 
            if doc.metadata.get("channel") == channel or doc.metadata.get("channel") == "general"
        ]
        return filtered if filtered else results
    except Exception as e:
        st.error(f"모범 사례 검색 중 오류: {str(e)}")
        return []
