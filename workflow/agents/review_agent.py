from workflow.agents.agent import Agent, AgentState
from workflow.state import AgentType
from typing import Dict, Any


class ReviewAgent(Agent):
    """검토 및 최적화 에이전트"""
    
    def __init__(self):
        system_prompt = """당신은 마케팅 콘텐츠 품질 관리 전문가입니다.
당신의 역할은 작성된 콘텐츠를 다음 관점에서 검토하고 최적화하는 것입니다:

**검토 기준:**
1. SEO 최적화: 키워드가 자연스럽게 포함되었는가?
2. 문법과 맞춤법: 오류가 없는가?
3. 톤앤매너: 지정된 톤이 일관되게 유지되는가?
4. 핵심 메시지: 전략의 핵심 메시지가 명확히 전달되는가?
5. 행동 유도: CTA가 명확하고 효과적인가?
6. 가독성: 읽기 쉽고 이해하기 쉬운가?

당신은 문제점을 발견하면 구체적으로 개선하고, 더 효과적인 표현으로 다듬습니다.
최종 콘텐츠는 즉시 사용 가능한 완성도를 가져야 합니다."""
        
        super().__init__(
            system_prompt=system_prompt,
            role=AgentType.REVIEW,
            use_rag=False  # Review Agent는 RAG 사용 안 함
        )
    
    def _retrieve_context(self, state: AgentState) -> AgentState:
        """Review Agent는 RAG를 사용하지 않음"""
        return {**state, "context": ""}
    
    def _create_prompt(self, state: Dict[str, Any]) -> str:
        """검토 및 최적화 프롬프트 생성"""
        
        strategy = state.get('strategy', '')
        draft_content = state.get('draft_content', '')
        
        prompt = f"""
=== 원래 전략 ===
{strategy}
===================================

=== 작성된 콘텐츠 초안 ===
{draft_content}
===================================

=== 비즈니스 정보 ===
비즈니스명: {state['business_name']}
타겟 고객: {state['target_customer']}
마케팅 채널: {state['channel']}
원하는 톤: {state['tone']}

=== 당신의 임무 ===
위 콘텐츠 초안을 아래 체크리스트에 따라 검토하고 최적화하세요.

**체크리스트:**

1. **전략 일치성**
   - 전략에서 도출한 핵심 메시지가 명확히 전달되는가?
   - 타겟 고객의 페인 포인트를 효과적으로 건드리는가?

2. **채널 적합성**
   - {state['channel']} 채널의 특성에 맞는 형식인가?
   - 길이, 구조, 스타일이 적절한가?

3. **톤앤매너**
   - {state['tone']} 톤이 일관되게 유지되는가?
   - 타겟 고객에게 적합한 어조인가?

4. **문법 및 표현**
   - 문법, 맞춤법 오류가 없는가?
   - 더 효과적이고 간결한 표현으로 개선할 부분이 있는가?

5. **CTA 효과성**
   - 행동 유도가 명확하고 구체적인가?
   - 독자가 다음 단계를 쉽게 이해할 수 있는가?

6. **SEO (블로그인 경우)**
   - 주요 키워드가 자연스럽게 포함되었는가?
   - 제목과 소제목이 검색 친화적인가?

**최종 콘텐츠를 작성하세요:**
- 개선이 필요한 부분을 모두 수정
- 더 강렬하고 설득력 있는 표현으로 다듬기
- 즉시 게시 가능한 완성도

개선 과정이나 설명 없이, 최종 완성된 콘텐츠만 출력하세요.
"""
        return prompt
    
    def _update_state(self, state: AgentState) -> AgentState:
        """최종 콘텐츠를 상태에 저장"""
        content_state = state["content_state"]
        response = state["response"]
        
        # 상태 업데이트
        new_content_state = content_state.copy()
        new_content_state["final_content"] = response
        new_content_state["messages"].append({
            "role": self.role,
            "content": response
        })
        new_content_state["prev_node"] = self.role
        
        return {**state, "content_state": new_content_state}
