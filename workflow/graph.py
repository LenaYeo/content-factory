from langgraph.graph import StateGraph, END
from workflow.state import ContentState, AgentType
from workflow.agents.strategy_agent import StrategyAgent
from workflow.agents.content_agent import ContentAgent
from workflow.agents.review_agent import ReviewAgent


def create_content_graph(enable_rag: bool = True):
    """
    마케팅 콘텐츠 생성 그래프 생성
    
    Flow: STRATEGY → CONTENT → REVIEW → END
    
    Args:
        enable_rag: RAG 활성화 여부
    
    Returns:
        컴파일된 LangGraph
    """
    
    # 그래프 생성
    workflow = StateGraph(ContentState)
    
    # 에이전트 인스턴스 생성
    strategy_agent = StrategyAgent(use_rag=enable_rag)
    content_agent = ContentAgent(use_rag=enable_rag)
    review_agent = ReviewAgent()  # Review는 항상 RAG 미사용
    
    # 노드 추가
    workflow.add_node(AgentType.STRATEGY, strategy_agent.run)
    workflow.add_node(AgentType.CONTENT, content_agent.run)
    workflow.add_node(AgentType.REVIEW, review_agent.run)
    
    # 엣지 추가 (순차 실행)
    workflow.add_edge(AgentType.STRATEGY, AgentType.CONTENT)
    workflow.add_edge(AgentType.CONTENT, AgentType.REVIEW)
    workflow.add_edge(AgentType.REVIEW, END)
    
    # 시작점 설정
    workflow.set_entry_point(AgentType.STRATEGY)
    
    # 그래프 컴파일
    return workflow.compile()


if __name__ == "__main__":
    """그래프 시각화 (개발/디버깅용)"""
    graph = create_content_graph(True)
    
    try:
        graph_image = graph.get_graph().draw_mermaid_png()
        
        output_path = "content_factory_graph.png"
        with open(output_path, "wb") as f:
            f.write(graph_image)
        
        print(f"Graph saved to {output_path}")
    except Exception as e:
        print(f"Could not visualize graph: {e}")
        print("Install graphviz for visualization: pip install pygraphviz")
