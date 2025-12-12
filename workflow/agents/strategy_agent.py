from workflow.agents.agent import Agent, AgentState, format_context_from_docs
from workflow.state import AgentType
from retrieval.vector_store import search_marketing_trends
from typing import Dict, Any


class StrategyAgent(Agent):
    """마케팅 전략 수립 에이전트"""
    
    def __init__(self, use_rag: bool = True):
        system_prompt = """당신은 세계적인 마케팅 전략 컨설턴트입니다. 
당신의 역할은 소규모 비즈니스를 위한 효과적인 마케팅 전략을 수립하는 것입니다.

당신은 다음 단계를 거쳐 전략을 수립합니다:
1. 타겟 고객 페르소나 분석 (니즈, 페인 포인트)
2. 비즈니스 특징을 고객 니즈에 연결한 핵심 메시지 도출
3. 선택된 채널의 특성에 맞는 톤앤매너 확정

논리적이고 구체적으로 사고하며, 최신 마케팅 트렌드를 반영합니다."""
        
        super().__init__(
            system_prompt=system_prompt,
            role=AgentType.STRATEGY,
            use_rag=use_rag
        )
    
    def _retrieve_context(self, state: AgentState) -> AgentState:
        """마케팅 트렌드 검색"""
        if not self.use_rag:
            return {**state, "context": ""}
        
        content_state = state["content_state"]
        
        # 검색 쿼리 생성
        query = f"{content_state['business_name']} {content_state['target_customer']} {content_state['channel']} 마케팅 트렌드"
        
        # RAG 검색
        docs = search_marketing_trends(query, k=2)
        
        # 검색된 문서 저장
        content_state["trend_docs"] = [doc.page_content for doc in docs] if docs else []
        
        # 컨텍스트 포맷팅
        context = format_context_from_docs(docs)
        
        return {**state, "content_state": content_state, "context": context}
    
    def _create_prompt(self, state: Dict[str, Any]) -> str:
        """Chain-of-Thought 프롬프트 생성"""
        context_section = ""
        if state.get("context"):
            context_section = f"""
=== 참고할 최신 마케팅 트렌드 ===
{state['context']}
===================================
"""
        
        prompt = f"""
{context_section}

=== 비즈니스 정보 ===
비즈니스명: {state['business_name']}
핵심 특징: {state['business_features']}
타겟 고객: {state['target_customer']}
마케팅 채널: {state['channel']}
원하는 톤: {state['tone']}

=== 당신의 임무 ===
위 정보를 바탕으로 Chain-of-Thought 방식으로 마케팅 전략을 수립하세요.

다음 단계를 순서대로 진행하며, 각 단계의 사고 과정을 보여주세요:

**1단계: 타겟 고객 페르소나 분석**
- 타겟 고객의 주요 니즈는 무엇인가?
- 타겟 고객의 페인 포인트(문제점)는 무엇인가?
- 이들은 어떤 가치를 추구하는가?

**2단계: 핵심 메시지 도출**
- 우리 비즈니스의 특징이 고객의 니즈를 어떻게 해결하는가?
- 경쟁사와 차별화되는 포인트는 무엇인가?
- 고객에게 전달해야 할 핵심 메시지는 무엇인가?

**3단계: 채널별 전략 확정**
- {state['channel']} 채널의 특성은 무엇인가?
- 이 채널에 적합한 톤앤매너는 무엇인가?
- 콘텐츠 구조는 어떻게 가져가야 하는가?

각 단계를 명확히 구분하여 작성하고, 구체적인 근거와 함께 결론을 도출하세요.
"""
        return prompt
    
    def _update_state(self, state: AgentState) -> AgentState:
        """전략 수립 결과를 상태에 저장"""
        content_state = state["content_state"]
        response = state["response"]
        
        # 상태 업데이트
        new_content_state = content_state.copy()
        new_content_state["strategy"] = response
        new_content_state["messages"].append({
            "role": self.role,
            "content": response
        })
        new_content_state["prev_node"] = self.role
        
        return {**state, "content_state": new_content_state}
