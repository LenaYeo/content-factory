# 🎨 AI 콘텐츠 팩토리 (Content Factory)

소규모 비즈니스를 위한 AI 기반 마케팅 콘텐츠 자동 생성기

## 📋 프로젝트 개요

Multi-Agent 시스템을 활용하여 전문적인 마케팅 콘텐츠를 자동으로 생성하는 서비스입니다. 3단계 워크플로우를 통해 전략 수립부터 최종 콘텐츠 검토까지 자동화합니다.

### 주요 기능

- **🧠 전략 수립 Agent**: Chain-of-Thought 방식으로 타겟 분석 및 핵심 메시지 도출
- **✍️ 콘텐츠 생성 Agent**: Few-shot Learning을 활용한 채널별 최적화 콘텐츠 작성
- **🔍 검토 최적화 Agent**: SEO, 문법, 톤앤매너 검증 및 최종 다듬기
- **📚 RAG 시스템**: 최신 마케팅 트렌드 및 채널별 모범 사례 검색
- **💾 히스토리 관리**: SQLite 기반 콘텐츠 생성 이력 저장

## 🏗️ 코드 구조

```
content_factory/
├── main.py                 # Streamlit 메인 앱
├── workflow/               # LangGraph 워크플로우
│   ├── graph.py           # Multi-Agent 그래프
│   └── agents/            # 3개 Agent (Strategy, Content, Review)
├── retrieval/             # RAG 시스템 (ChromaDB)
├── database/              # SQLite 데이터베이스
├── utils/                 # LLM 설정 (Azure OpenAI)
└── components/            # UI 컴포넌트
```

## 🚀 빠른 시작

### 1. 설치

```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정

`.env` 파일 생성:

```env
AOAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AOAI_API_KEY=your-api-key
AOAI_DEPLOY_GPT4O=gpt-4o
AOAI_DEPLOY_EMBED_3_LARGE=text-embedding-3-large
AOAI_API_VERSION=2024-02-15-preview
```

### 3. 실행

```bash
streamlit run main.py
```

브라우저에서 `http://localhost:8501` 접속

## 🎯 사용 방법

1. 사이드바에서 비즈니스 정보 입력 (비즈니스명, 특징, 타겟 고객, 채널, 톤)
2. RAG 활성화 선택 (선택사항)
3. '콘텐츠 생성' 버튼 클릭
4. 결과 확인 (전략 → 초안 → 최종 콘텐츠)

## 🔧 기술 스택

- **LangGraph**: Multi-Agent 워크플로우 (Strategy → Content → Review)
- **Azure OpenAI**: LLM (gpt-4o) 및 Embeddings (text-embedding-3-large)
- **ChromaDB**: 벡터 저장소 (RAG)
- **SQLite**: 히스토리 저장
- **Streamlit**: 웹 UI

## 📊 Agent 구조

- **Strategy Agent**: 트렌드 검색 → Chain-of-Thought 전략 수립
- **Content Agent**: 모범 사례 검색 → Few-shot 초안 작성
- **Review Agent**: 품질 검토 → 최종 최적화
