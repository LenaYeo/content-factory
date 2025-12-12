from abc import ABC, abstractmethod
from typing import Dict, Any, List, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END
from utils.config import get_llm
from workflow.state import ContentState


class AgentState(TypedDict):
    """에이전트 내부 상태"""
    content_state: Dict[str, Any]  # 전체 콘텐츠 생성 상태
    context: str  # 검색된 컨텍스트
    messages: List[BaseMessage]  # LLM에 전달할 메시지
    response: str  # LLM 응답


class Agent(ABC):
    """마케팅 콘텐츠 생성 에이전트 추상 클래스"""
    
    def __init__(self, system_prompt: str, role: str, use_rag: bool = True):
        """
        Args:
            system_prompt: 시스템 프롬프트
            role: 에이전트 역할 (STRATEGY_AGENT, CONTENT_AGENT, REVIEW_AGENT)
            use_rag: RAG 사용 여부
        """
        self.system_prompt = system_prompt
        self.role = role
        self.use_rag = use_rag
        self._setup_graph()
    
    def _setup_graph(self):
        """에이전트 내부 그래프 설정"""
        workflow = StateGraph(AgentState)
        
        # 노드 추가
        workflow.add_node("retrieve_context", self._retrieve_context)
        workflow.add_node("prepare_messages", self._prepare_messages)
        workflow.add_node("generate_response", self._generate_response)
        workflow.add_node("update_state", self._update_state)
        
        # 엣지 추가 - 순차 실행
        workflow.add_edge("retrieve_context", "prepare_messages")
        workflow.add_edge("prepare_messages", "generate_response")
        workflow.add_edge("generate_response", "update_state")
        
        workflow.set_entry_point("retrieve_context")
        workflow.add_edge("update_state", END)
        
        # 그래프 컴파일
        self.graph = workflow.compile()
    
    @abstractmethod
    def _retrieve_context(self, state: AgentState) -> AgentState:
        """
        RAG를 통해 관련 컨텍스트 검색
        하위 클래스에서 구현 필요
        """
        pass
    
    def _prepare_messages(self, state: AgentState) -> AgentState:
        """LLM에 전달할 메시지 준비"""
        content_state = state["content_state"]
        context = state["context"]
        
        # 시스템 프롬프트
        messages = [SystemMessage(content=self.system_prompt)]
        
        # 기존 대화 기록 추가
        for message in content_state["messages"]:
            if message["role"] == "assistant":
                messages.append(AIMessage(content=message["content"]))
            else:
                messages.append(
                    HumanMessage(content=f"{message['role']}: {message['content']}")
                )
        
        # 프롬프트 생성
        prompt = self._create_prompt({**content_state, "context": context})
        messages.append(HumanMessage(content=prompt))
        
        return {**state, "messages": messages}
    
    @abstractmethod
    def _create_prompt(self, state: Dict[str, Any]) -> str:
        """
        프롬프트 생성
        하위 클래스에서 구현 필요
        """
        pass
    
    def _generate_response(self, state: AgentState) -> AgentState:
        """LLM 호출하여 응답 생성"""
        messages = state["messages"]
        llm = get_llm(temperature=0.7)
        response = llm.invoke(messages)
        
        return {**state, "response": response.content}
    
    @abstractmethod
    def _update_state(self, state: AgentState) -> AgentState:
        """
        상태 업데이트
        하위 클래스에서 구현 필요
        """
        pass
    
    def run(self, state: ContentState) -> ContentState:
        """에이전트 실행"""
        # 초기 에이전트 상태 구성
        agent_state = AgentState(
            content_state=state,
            context="",
            messages=[],
            response=""
        )
        
        # 내부 그래프 실행
        result = self.graph.invoke(agent_state)
        
        # 최종 콘텐츠 상태 반환
        return result["content_state"]


def format_context_from_docs(docs: List) -> str:
    """검색된 문서들을 컨텍스트 문자열로 포맷팅"""
    if not docs:
        return ""
    
    context = ""
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "Unknown")
        category = doc.metadata.get("category", "")
        channel = doc.metadata.get("channel", "")
        
        context += f"[참고자료 {i + 1}]"
        if source != "Unknown":
            context += f" 출처: {source}"
        if category:
            context += f", 카테고리: {category}"
        if channel:
            context += f", 채널: {channel}"
        context += f"\n{doc.page_content}\n\n"
    
    return context
