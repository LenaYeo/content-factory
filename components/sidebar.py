import streamlit as st
from database.repository import content_repository
import json


def render_sidebar():
    """사이드바 렌더링 - 입력 폼 및 히스토리"""
    
    with st.sidebar:
        st.header("🎨 콘텐츠 팩토리")
        
        # 탭 구성
        tab1, tab2 = st.tabs(["새 콘텐츠 생성", "히스토리"])
        
        with tab1:
            render_input_form()
        
        with tab2:
            render_history()


def render_input_form():
    """콘텐츠 생성 입력 폼"""
    
    st.subheader("비즈니스 정보")
    
    # 비즈니스명
    business_name = st.text_input(
        "비즈니스/제품명 *",
        value=st.session_state.get("business_name", ""),
        placeholder="예: 유기농 화장품 브랜드"
    )
    
    # 핵심 특징
    business_features = st.text_area(
        "핵심 특징 *",
        value=st.session_state.get("business_features", ""),
        placeholder="예: 국내산 유기농 원료만 사용, 동물실험 반대, 친환경 패키징",
        height=100
    )
    
    # 타겟 고객
    target_customer = st.text_input(
        "타겟 고객 *",
        value=st.session_state.get("target_customer", ""),
        placeholder="예: 20-30대 환경을 중시하는 여성"
    )
    
    st.subheader("마케팅 설정")
    
    # 채널 선택
    channel = st.selectbox(
        "마케팅 채널 *",
        options=["instagram", "blog", "email"],
        format_func=lambda x: {
            "instagram": "📸 인스타그램",
            "blog": "📝 블로그",
            "email": "📧 이메일"
        }[x],
        index=["instagram", "blog", "email"].index(
            st.session_state.get("channel", "instagram")
        )
    )
    
    # 톤앤매너
    tone = st.selectbox(
        "톤앤매너 *",
        options=["친근한", "전문적인", "감성적인", "유머러스한"],
        index=["친근한", "전문적인", "감성적인", "유머러스한"].index(
            st.session_state.get("tone", "친근한")
        )
    )
    
    # RAG 활성화
    enable_rag = st.checkbox(
        "🔍 RAG 활성화 (트렌드 및 모범 사례 검색)",
        value=st.session_state.get("enable_rag", True),
        help="최신 마케팅 트렌드와 채널별 모범 사례를 검색하여 더 효과적인 콘텐츠를 생성합니다."
    )
    
    st.divider()
    
    # 생성 버튼
    if st.button("🚀 콘텐츠 생성", use_container_width=True, type="primary"):
        # 필수 필드 검증
        if not business_name or not business_features or not target_customer:
            st.error("모든 필수 항목(*)을 입력해주세요.")
            return
        
        # 세션 상태 업데이트
        st.session_state.business_name = business_name
        st.session_state.business_features = business_features
        st.session_state.target_customer = target_customer
        st.session_state.channel = channel
        st.session_state.tone = tone
        st.session_state.enable_rag = enable_rag
        st.session_state.app_mode = "generating"
        st.session_state.viewing_history = False
        
        st.rerun()


def render_history():
    """히스토리 목록 렌더링"""
    
    st.subheader("생성 히스토리")
    
    # 히스토리 조회
    histories = content_repository.get_all(limit=20)
    
    if not histories:
        st.info("아직 생성된 콘텐츠가 없습니다.")
        return
    
    # 검색
    search_query = st.text_input("🔍 비즈니스명 검색", key="history_search")
    
    if search_query:
        histories = [h for h in histories if search_query.lower() in h.business_name.lower()]
    
    # 히스토리 목록
    for history in histories:
        channel_emoji = {
            "instagram": "📸",
            "blog": "📝",
            "email": "📧"
        }.get(history.channel, "📄")
        
        with st.expander(f"{channel_emoji} {history.business_name} - {history.date}"):
            st.write(f"**타겟 고객:** {history.target_customer}")
            st.write(f"**채널:** {history.channel}")
            st.write(f"**톤:** {history.tone}")
            
            if st.button("이 콘텐츠 보기", key=f"view_{history.id}"):
                # 히스토리 로드
                st.session_state.loaded_history = history
                st.session_state.app_mode = "results"
                st.session_state.viewing_history = True
                st.rerun()
