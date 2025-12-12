from workflow.agents.agent import Agent, AgentState, format_context_from_docs
from workflow.state import AgentType
from retrieval.vector_store import search_best_practices
from typing import Dict, Any


class ContentAgent(Agent):
    """콘텐츠 생성 에이전트"""
    
    def __init__(self, use_rag: bool = True):
        system_prompt = """당신은 세계적인 전문 카피라이터입니다.
당신의 역할은 수립된 마케팅 전략을 바탕으로 즉시 사용 가능한 고품질 마케팅 콘텐츠를 작성하는 것입니다.

당신의 작성 원칙:
- 전략에서 도출된 핵심 메시지를 명확히 전달
- 타겟 고객의 감성과 니즈에 공감
- 채널 특성에 맞는 형식과 톤앤매너 적용
- 구체적이고 행동을 유도하는 문구 사용
- 모범 사례의 구조를 참고하되, 창의적으로 재구성

매력적이고 설득력 있는 콘텐츠를 작성하세요."""
        
        super().__init__(
            system_prompt=system_prompt,
            role=AgentType.CONTENT,
            use_rag=use_rag
        )
    
    def _retrieve_context(self, state: AgentState) -> AgentState:
        """채널별 모범 사례 검색"""
        if not self.use_rag:
            return {**state, "context": ""}
        
        content_state = state["content_state"]
        channel = content_state['channel']
        
        # RAG 검색
        docs = search_best_practices(channel, k=2)
        
        # 검색된 문서 저장
        content_state["best_practice_docs"] = [doc.page_content for doc in docs] if docs else []
        
        # 컨텍스트 포맷팅
        context = format_context_from_docs(docs)
        
        return {**state, "content_state": content_state, "context": context}
    
    def _create_prompt(self, state: Dict[str, Any]) -> str:
        """Few-shot Prompting을 활용한 프롬프트 생성"""
        
        # 전략 정보
        strategy = state.get('strategy', '')
        
        # 모범 사례 정보
        context_section = ""
        if state.get("context"):
            context_section = f"""
=== {state['channel']} 채널 모범 사례 ===
{state['context']}
위 모범 사례의 구조와 형식을 참고하되, 그대로 복사하지 말고 창의적으로 재구성하세요.
===================================
"""
        
        prompt = f"""
=== 수립된 마케팅 전략 ===
{strategy}
===================================

{context_section}

=== 비즈니스 정보 ===
비즈니스명: {state['business_name']}
핵심 특징: {state['business_features']}
타겟 고객: {state['target_customer']}
마케팅 채널: {state['channel']}
원하는 톤: {state['tone']}

=== 당신의 임무 ===
위의 전략을 바탕으로 {state['channel']} 채널에 즉시 게시할 수 있는 마케팅 콘텐츠 초안을 작성하세요.

**작성 지침:**
1. 전략에서 도출한 핵심 메시지를 반드시 포함
2. 타겟 고객의 페인 포인트를 언급하고 솔루션 제시
3. 모범 사례의 구조를 참고하여 효과적인 형식 사용
4. {state['tone']} 톤으로 작성
5. 명확한 CTA(Call To Action) 포함

**채널별 요구사항:**
"""
        
        # 채널별 구체적 지침
        if state['channel'] == 'instagram':
            prompt += """
- 첫 문장에서 강렬하게 주목 끌기
- 2-3개 단락으로 간결하게 구성
- 이모지 활용하여 시각적 흥미 유발
- 5-8개의 관련 해시태그 포함
- 스토리텔링 또는 감성적 연결 강조
"""
        elif state['channel'] == 'blog':
            prompt += """
- 제목: 호기심을 자극하는 질문 또는 숫자 활용
- 구조: 도입(문제 제시) → 본문(해결책) → 결론(행동 촉구)
- 최소 500자 이상 작성
- 소제목을 활용하여 가독성 향상
- SEO를 고려한 키워드 자연스럽게 배치
"""
        elif state['channel'] == 'email':
            prompt += """
- 제목: 40자 이내, 긴급성/혜택/호기심 중 하나 강조
- 개인화된 인사로 시작
- 핵심 메시지를 3줄 이내로 명확하게 전달
- 혜택을 bullet points로 간결하게 나열
- 하나의 명확한 CTA 버튼/링크
"""
        
        prompt += "\n\n완성도 높은 콘텐츠 초안을 작성하세요."
        
        return prompt
    
    def _update_state(self, state: AgentState) -> AgentState:
        """콘텐츠 초안을 상태에 저장"""
        content_state = state["content_state"]
        response = state["response"]
        
        # 상태 업데이트
        new_content_state = content_state.copy()
        new_content_state["draft_content"] = response
        new_content_state["messages"].append({
            "role": self.role,
            "content": response
        })
        new_content_state["prev_node"] = self.role
        
        return {**state, "content_state": new_content_state}
