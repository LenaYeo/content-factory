import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langfuse import Langfuse

# .env 파일에서 환경 변수 로드
load_dotenv()


def get_llm(temperature: float = 0.7):
    """LLM 인스턴스 반환 - Azure OpenAI 사용"""
    return AzureChatOpenAI(
        openai_api_key=os.getenv("AOAI_API_KEY"),
        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
        azure_deployment=os.getenv("AOAI_DEPLOY_GPT4O"),
        api_version=os.getenv("AOAI_API_VERSION"),
        temperature=temperature,
    )


def get_embeddings():
    """Embeddings 인스턴스 반환 - Azure OpenAI 사용"""
    return AzureOpenAIEmbeddings(
        model=os.getenv("AOAI_DEPLOY_EMBED_3_LARGE"),
        openai_api_version=os.getenv("AOAI_API_VERSION"),
        api_key=os.getenv("AOAI_API_KEY"),
        azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    )


def get_langfuse():
    """Langfuse 인스턴스 반환 (선택사항)"""
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    host = os.getenv("LANGFUSE_BASE_URL")
    
    # Langfuse 설정이 모두 있으면 인스턴스 생성, 없으면 None 반환
    if secret_key and public_key and host:
        return Langfuse(
            secret_key=secret_key,
            public_key=public_key,
            host=host,
        )
    return None


# Langfuse 인스턴스 생성 (선택사항)
langfuse = get_langfuse()


# 환경변수 검증
def validate_env():
    """필수 환경변수 확인"""
    endpoint = os.getenv("AOAI_ENDPOINT")
    api_key = os.getenv("AOAI_API_KEY")
    deployment_name = os.getenv("AOAI_DEPLOY_GPT4O")
    embedding_deployment = os.getenv("AOAI_DEPLOY_EMBED_3_LARGE")
    api_version = os.getenv("AOAI_API_VERSION")
    
    missing_vars = []
    if not endpoint:
        missing_vars.append("AOAI_ENDPOINT")
    if not api_key:
        missing_vars.append("AOAI_API_KEY")
    if not deployment_name:
        missing_vars.append("AOAI_DEPLOY_GPT4O")
    if not embedding_deployment:
        missing_vars.append("AOAI_DEPLOY_EMBED_3_LARGE")
    if not api_version:
        missing_vars.append("AOAI_API_VERSION")
    
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            "Please check your .env file.\n"
            "Required variables:\n"
            "- AOAI_ENDPOINT: Azure OpenAI endpoint URL\n"
            "- AOAI_API_KEY: Azure OpenAI API key\n"
            "- AOAI_DEPLOY_GPT4O: Azure OpenAI deployment name for chat model\n"
            "- AOAI_DEPLOY_EMBED_3_LARGE: Azure OpenAI deployment name for embeddings\n"
            "- AOAI_API_VERSION: Azure OpenAI API version\n"
            "Optional variables (Langfuse):\n"
            "- LANGFUSE_SECRET_KEY: Langfuse secret key\n"
            "- LANGFUSE_PUBLIC_KEY: Langfuse public key\n"
            "- LANGFUSE_BASE_URL: Langfuse base URL"
        )
