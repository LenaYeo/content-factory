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

## 🏗️ 시스템 아키텍처

```
content_factory/
├── main.py                      # Streamlit 메인 앱
├── .env                         # 환경변수 설정
├── requirements.txt             # Python 패키지 의존성
│
├── utils/                       # 유틸리티
│   ├── __init__.py
│   └── config.py               # LLM 및 Embeddings 설정
│
├── workflow/                    # LangGraph 워크플로우
│   ├── __init__.py
│   ├── state.py                # 상태 정의
│   ├── graph.py                # 그래프 구성
│   └── agents/                 # Agent 구현
│       ├── __init__.py
│       ├── agent.py            # 추상 Base Agent
│       ├── strategy_agent.py   # 전략 수립 Agent
│       ├── content_agent.py    # 콘텐츠 생성 Agent
│       └── review_agent.py     # 검토 최적화 Agent
│
├── retrieval/                   # RAG 시스템
│   ├── __init__.py
│   └── vector_store.py         # ChromaDB 벡터 저장소
│
├── database/                    # 데이터베이스
│   ├── __init__.py
│   ├── model.py                # SQLAlchemy 모델
│   ├── session.py              # DB 세션 관리
│   └── repository.py           # Repository 패턴
│
├── components/                  # UI 컴포넌트
│   ├── __init__.py
│   └── sidebar.py              # 사이드바 (입력폼, 히스토리)
│
└── data/                        # 데이터 저장소
    └── chroma_db/              # ChromaDB 영구 저장소

```

## 🚀 시작하기

### 1. 환경 설정

```bash
# 저장소 클론 또는 다운로드
cd content_factory

# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 환경변수 설정

`.env` 파일을 생성하고 Azure OpenAI 설정을 추가합니다:

```env
# Azure OpenAI 필수 설정
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-openai-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Azure OpenAI 선택 설정
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=text-embedding-3-large

# 데이터베이스 설정
DB_PATH=content_history.db
```

### 3. 실행

```bash
streamlit run main.py
```

브라우저에서 `http://localhost:8501` 접속

## 🎯 사용 방법

### 콘텐츠 생성

1. **사이드바에서 비즈니스 정보 입력**
   - 비즈니스/제품명
   - 핵심 특징
   - 타겟 고객
   - 마케팅 채널 (인스타그램/블로그/이메일)
   - 톤앤매너 (친근한/전문적인/감성적인/유머러스한)

2. **RAG 활성화 선택** (선택사항)
   - 최신 마케팅 트렌드 검색
   - 채널별 모범 사례 참조

3. **'콘텐츠 생성' 버튼 클릭**

4. **결과 확인**
   - 전략 수립 과정
   - 최종 콘텐츠
   - 참고 자료

### 히스토리 관리

- 사이드바 "히스토리" 탭에서 이전 생성 결과 조회
- 비즈니스명으로 검색 가능
- 클릭하여 이전 콘텐츠 재확인

## 🔧 핵심 기술 스택

### 1. Prompt Engineering

- **역할 부여 (Role Assignment)**: 각 Agent에 명확한 역할과 전문성 부여
- **Chain-of-Thought**: 전략 Agent가 단계별 사고 과정을 거쳐 논리적 전략 수립
- **Few-shot Prompting**: 모범 사례 검색 결과를 프롬프트에 포함하여 효과적인 형식 학습

### 2. LangChain & LangGraph

```python
# Multi-Agent 워크플로우
StateGraph:
  STRATEGY_AGENT → CONTENT_AGENT → REVIEW_AGENT → END

# 각 Agent는 내부 Subgraph 보유
Agent Subgraph:
  retrieve_context → prepare_messages → generate_response → update_state
```

- **LangGraph**: 복잡한 Multi-Agent 워크플로우 관리
- **State Management**: TypedDict 기반 상태 정의 및 추적
- **Streaming**: 각 Agent의 진행 상황 실시간 표시

### 3. RAG (Retrieval-Augmented Generation)

```python
# Vector Store
ChromaDB:
  - marketing_trends: 최신 마케팅 트렌드 5개
  - best_practices: 채널별 모범 사례 4개

# Embeddings
Azure OpenAI text-embedding-3-large

# Retrieval
k=2 (Agent당 상위 2개 문서 검색)
```

### 4. 데이터베이스

- **SQLite**: 경량 파일 기반 데이터베이스
- **SQLAlchemy ORM**: 객체 관계 매핑
- **Repository Pattern**: 데이터 접근 계층 추상화

## 📊 Agent 상세 설명

### 1️⃣ 전략 수립 Agent (Strategy Agent)

**역할**: 마케팅 전략 컨설턴트

**프로세스**:
1. RAG를 통해 최신 마케팅 트렌드 검색
2. Chain-of-Thought 방식으로 사고:
   - 타겟 고객 페르소나 분석 (니즈, 페인 포인트)
   - 비즈니스 특징을 고객 니즈에 연결한 핵심 메시지 도출
   - 채널 특성에 맞는 톤앤매너 확정

**출력**: 구조화된 마케팅 전략 문서

### 2️⃣ 콘텐츠 생성 Agent (Content Agent)

**역할**: 전문 카피라이터

**프로세스**:
1. RAG를 통해 채널별 모범 사례 검색
2. Few-shot Learning 적용:
   - 모범 사례 구조 참고
   - 전략의 핵심 메시지 반영
   - 채널별 최적화 (길이, 형식, 스타일)

**출력**: 즉시 사용 가능한 마케팅 콘텐츠 초안

### 3️⃣ 검토 최적화 Agent (Review Agent)

**역할**: 품질 관리 전문가

**프로세스**:
1. 6가지 기준으로 검토:
   - 전략 일치성
   - 채널 적합성
   - 톤앤매너 일관성
   - 문법 및 표현
   - CTA 효과성
   - SEO 최적화 (블로그)
2. 문제점 발견 및 개선

**출력**: 최종 검수된 완성 콘텐츠

## 🐳 Docker 배포 (선택사항)

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 복사
COPY . .

# Streamlit 포트
EXPOSE 8501

# 실행
CMD ["streamlit", "run", "main.py", "--server.address", "0.0.0.0"]
```

### 실행

```bash
# 이미지 빌드
docker build -t content-factory .

# 컨테이너 실행
docker run -p 8501:8501 --env-file .env content-factory
```

## 🔐 환경변수 관리

**필수 환경변수**:
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI 엔드포인트 URL (예: https://your-resource-name.openai.azure.com/)
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API 키
- `AZURE_OPENAI_DEPLOYMENT_NAME`: Azure OpenAI 배포 이름 (채팅 모델용)

**선택 환경변수**:
- `AZURE_OPENAI_API_VERSION`: API 버전 (기본값: 2024-02-15-preview)
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME`: Embedding 모델 배포 이름 (기본값: text-embedding-3-large)
- `DB_PATH`: 데이터베이스 파일 경로 (기본값: content_history.db)

**주의사항**:
- `.env` 파일은 절대 Git에 커밋하지 않기
- `.gitignore`에 `.env` 추가
- API 키는 안전하게 관리
- Azure OpenAI 리소스가 생성되어 있고 배포가 완료되어 있어야 합니다

## 📈 확장 가능성

### 추가 기능 아이디어

1. **더 많은 채널 지원**
   - LinkedIn, Facebook, Twitter 등
   - 각 채널별 모범 사례 추가

2. **A/B 테스트 기능**
   - 동일 전략으로 여러 버전 생성
   - 성과 비교 및 학습

3. **이미지 생성 통합**
   - DALL-E 연동
   - 콘텐츠에 맞는 이미지 자동 생성

4. **다국어 지원**
   - 영어, 일본어 등 다양한 언어
   - 문화적 맥락 고려

5. **API 서버 구축**
   - FastAPI로 REST API 제공
   - 외부 서비스 통합 가능

## 🤝 기여 방법

1. Fork 프로젝트
2. Feature 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경사항 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 Push (`git push origin feature/AmazingFeature`)
5. Pull Request 생성

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 📧 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 Issue를 생성해주세요.

---

**Made with ❤️ using LangChain, LangGraph, and Streamlit**
