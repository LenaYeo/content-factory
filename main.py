import streamlit as st
from components.sidebar import render_sidebar
from workflow.state import AgentType, ContentState
from workflow.graph import create_content_graph
from database.session import db_session
from database.repository import content_repository
from utils.config import validate_env
import json


def init_session_state():
    """세션 상태 초기화"""
    defaults = {
        "app_mode": "input",  # input, generating, results
        "business_name": "",
        "business_features": "",
        "target_customer": "",
        "channel": "instagram",
        "tone": "친근한",
        "enable_rag": True,
        "viewing_history": False,
        "loaded_history": None,
        "current_strategy": None,
        "current_draft": None,
        "current_final": None,
        "trend_docs": [],
        "best_practice_docs": []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_session_state():
    """세션 상태 리셋"""
    st.session_state.app_mode = "input"
    st.session_state.viewing_history = False
    st.session_state.current_strategy = None
    st.session_state.current_draft = None
    st.session_state.current_final = None
    st.session_state.trend_docs = []
    st.session_state.best_practice_docs = []


def generate_content():
    """콘텐츠 생성 실행"""
    
    # 그래프 생성
    content_graph = create_content_graph(st.session_state.enable_rag)
    
    # 초기 상태 설정
    initial_state: ContentState = {
        "business_name": st.session_state.business_name,
        "business_features": st.session_state.business_features,
        "target_customer": st.session_state.target_customer,
        "channel": st.session_state.channel,
        "tone": st.session_state.tone,
        "messages": [],
        "strategy": None,
        "draft_content": None,
        "final_content": None,
        "trend_docs": [],
        "best_practice_docs": [],
        "prev_node": "START"
    }
    
    # 콘텐츠 생성 시작
    with st.spinner("🎨 AI가 마케팅 콘텐츠를 생성하고 있습니다... 잠시만 기다려주세요."):
        
        # 스트리밍으로 각 Agent의 진행 상황 표시
        for chunk in content_graph.stream(
            initial_state,
            stream_mode="updates"
        ):
            process_generation_chunk(chunk)
    
    # 결과 저장
    if st.session_state.current_final:
        content_repository.save(
            business_name=st.session_state.business_name,
            target_customer=st.session_state.target_customer,
            channel=st.session_state.channel,
            tone=st.session_state.tone,
            strategy=st.session_state.current_strategy or "",
            final_content=st.session_state.current_final,
            trend_docs=st.session_state.trend_docs,
            best_practice_docs=st.session_state.best_practice_docs
        )


def process_generation_chunk(chunk):
    """생성 과정 중 각 Agent의 결과 처리"""
    if not chunk:
        return
    
    # Agent 타입 추출
    agent_type = list(chunk.keys())[0]
    state = chunk[agent_type]
    
    # 각 Agent별 처리
    if agent_type == AgentType.STRATEGY:
        st.session_state.current_strategy = state.get("strategy")
        st.session_state.trend_docs = state.get("trend_docs", [])
        
        with st.expander("1️⃣ 전략 수립 완료", expanded=True):
            st.markdown(state.get("strategy", ""))
        
    elif agent_type == AgentType.CONTENT:
        st.session_state.current_draft = state.get("draft_content")
        st.session_state.best_practice_docs = state.get("best_practice_docs", [])
        
        with st.expander("2️⃣ 콘텐츠 초안 생성 완료", expanded=True):
            st.markdown(state.get("draft_content", ""))
    
    elif agent_type == AgentType.REVIEW:
        st.session_state.current_final = state.get("final_content")
        st.session_state.app_mode = "results"
        
        with st.expander("3️⃣ 검토 및 최적화 완료", expanded=True):
            st.success("✅ 최종 콘텐츠가 생성되었습니다!")


def display_results():
    """결과 화면 표시"""
    
    # 히스토리 보기 모드인지 확인
    if st.session_state.viewing_history and st.session_state.loaded_history:
        history = st.session_state.loaded_history
        
        st.info("📚 저장된 히스토리를 보고 있습니다.")
        
        # 히스토리에서 정보 로드
        st.header(f"🎯 {history.business_name}")
        st.write(f"**타겟 고객:** {history.target_customer}")
        st.write(f"**채널:** {history.channel} | **톤:** {history.tone}")
        st.write(f"**생성 날짜:** {history.date}")
        
        st.divider()
        
        # 전략 표시
        if history.strategy:
            with st.expander("📊 마케팅 전략"):
                st.markdown(history.strategy)
        
        # 최종 콘텐츠
        st.subheader("✨ 최종 콘텐츠")
        st.markdown("---")
        st.markdown(history.final_content)
        st.markdown("---")
        
        # 복사 버튼
        st.code(history.final_content, language=None)
        
        # RAG 참고 자료
        if history.trend_docs or history.best_practice_docs:
            render_reference_materials(
                json.loads(history.trend_docs) if history.trend_docs else [],
                json.loads(history.best_practice_docs) if history.best_practice_docs else []
            )
    
    else:
        # 새로 생성된 콘텐츠
        st.success("✅ 콘텐츠 생성이 완료되었습니다!")
        
        st.header(f"🎯 {st.session_state.business_name}")
        st.write(f"**타겟 고객:** {st.session_state.target_customer}")
        st.write(f"**채널:** {st.session_state.channel} | **톤:** {st.session_state.tone}")
        
        st.divider()
        
        # 전략 표시
        if st.session_state.current_strategy:
            with st.expander("📊 마케팅 전략", expanded=False):
                st.markdown(st.session_state.current_strategy)
        
        # 최종 콘텐츠
        st.subheader("✨ 최종 콘텐츠")
        st.markdown("---")
        st.markdown(st.session_state.current_final)
        st.markdown("---")
        
        # 복사 버튼
        st.code(st.session_state.current_final, language=None)
        
        # RAG 참고 자료
        if st.session_state.trend_docs or st.session_state.best_practice_docs:
            render_reference_materials(
                st.session_state.trend_docs,
                st.session_state.best_practice_docs
            )
    
    # 액션 버튼
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 새 콘텐츠 생성", use_container_width=True):
            reset_session_state()
            st.rerun()
    
    with col2:
        if st.button("📝 수정 요청", use_container_width=True):
            st.info("💡 사이드바에서 설정을 변경하고 다시 생성해보세요!")


def render_reference_materials(trend_docs, best_practice_docs):
    """RAG 참고 자료 표시"""
    
    with st.expander("📚 사용된 참고 자료"):
        if trend_docs:
            st.subheader("최신 마케팅 트렌드")
            for i, doc in enumerate(trend_docs[:3]):
                st.markdown(f"**문서 {i+1}**")
                st.text(doc[:200] + "..." if len(doc) > 200 else doc)
                st.divider()
        
        if best_practice_docs:
            st.subheader("채널별 모범 사례")
            for i, doc in enumerate(best_practice_docs[:3]):
                st.markdown(f"**문서 {i+1}**")
                st.text(doc[:200] + "..." if len(doc) > 200 else doc)
                st.divider()


def render_ui():
    """메인 UI 렌더링"""
    
    # 페이지 설정
    st.set_page_config(
        page_title="AI 콘텐츠 팩토리",
        page_icon="🎨",
        layout="wide"
    )
    
    # 제목 및 소개
    st.title("🎨 AI 콘텐츠 팩토리")
    st.markdown("""
    ### 소규모 비즈니스를 위한 AI 기반 마케팅 콘텐츠 자동 생성기
    
    **Multi-Agent 시스템**이 3단계로 전문적인 마케팅 콘텐츠를 생성합니다:
    1. 🧠 **전략 수립**: 타겟 분석 및 핵심 메시지 도출
    2. ✍️ **콘텐츠 생성**: 채널별 최적화된 초안 작성
    3. 🔍 **검토 최적화**: SEO 및 품질 검증
    """)
    
    # 사이드바 렌더링
    render_sidebar()
    
    # 현재 모드에 따라 화면 전환
    current_mode = st.session_state.get("app_mode")
    
    if current_mode == "generating":
        generate_content()
    elif current_mode == "results":
        display_results()
    else:
        # 초기 화면
        st.info("👈 사이드바에서 비즈니스 정보를 입력하고 '콘텐츠 생성' 버튼을 클릭하세요!")
        
        # 기능 소개
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🎯 Prompt Engineering")
            st.write("- Chain-of-Thought 전략 수립")
            st.write("- Few-shot Learning 활용")
            st.write("- 역할 기반 프롬프트")
        
        with col2:
            st.markdown("### 🤖 Multi-Agent Flow")
            st.write("- LangGraph 기반 워크플로우")
            st.write("- 3단계 순차 처리")
            st.write("- 상태 관리 및 추적")
        
        with col3:
            st.markdown("### 📚 RAG 시스템")
            st.write("- ChromaDB 벡터 저장소")
            st.write("- 마케팅 트렌드 검색")
            st.write("- 채널별 모범 사례 참조")


if __name__ == "__main__":
    try:
        # 환경변수 검증
        validate_env()
        
        # 세션 상태 초기화
        init_session_state()
        
        # 데이터베이스 초기화
        db_session.initialize()
        
        # UI 렌더링
        render_ui()
        
    except ValueError as e:
        st.error(f"❌ 환경 설정 오류: {str(e)}")
        st.info("💡 .env 파일에 KEY를 설정해주세요.")
    except Exception as e:
        st.error(f"❌ 오류 발생: {str(e)}")
        st.exception(e)
