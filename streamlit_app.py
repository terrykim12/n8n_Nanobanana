import streamlit as st
import os
from dotenv import load_dotenv
from ai_assistant import AIAssistant

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="AI 비서",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'assistant' not in st.session_state:
    st.session_state.assistant = None

def initialize_assistant():
    """AI 비서를 초기화합니다."""
    if os.getenv("OPENAI_API_KEY"):
        try:
            st.session_state.assistant = AIAssistant()
            return True
        except Exception as e:
            st.error(f"AI 비서 초기화 중 오류가 발생했습니다: {str(e)}")
            return False
    else:
        st.error("OpenAI API 키가 설정되지 않았습니다.")
        return False

def main():
    st.title("🤖 AI 비서")
    st.markdown("Crew AI를 사용한 지능형 AI 비서입니다.")
    
    # 사이드바
    with st.sidebar:
        st.header("⚙️ 설정")
        
        # API 키 입력
        api_key = st.text_input(
            "OpenAI API 키",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="OpenAI API 키를 입력하세요"
        )
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        # 초기화 버튼
        if st.button("🔄 AI 비서 초기화"):
            if initialize_assistant():
                st.success("AI 비서가 성공적으로 초기화되었습니다!")
            else:
                st.error("AI 비서 초기화에 실패했습니다.")
        
        st.markdown("---")
        st.markdown("### 📚 사용법")
        st.markdown("""
        1. OpenAI API 키를 입력하세요
        2. AI 비서 초기화 버튼을 클릭하세요
        3. 채팅창에 질문을 입력하세요
        
        **간단한 질문**: 빠른 응답
        **복잡한 작업**: 여러 에이전트가 협력하여 처리
        """)
        
        st.markdown("---")
        st.markdown("### 🧠 에이전트 구성")
        st.markdown("""
        - **AI 비서**: 메인 조정자
        - **연구원**: 정보 수집
        - **분석가**: 데이터 분석
        - **작성자**: 콘텐츠 작성
        """)
    
    # 메인 채팅 영역
    if st.session_state.assistant is None:
        st.info("👈 사이드바에서 OpenAI API 키를 입력하고 AI 비서를 초기화하세요.")
        return
    
    # 채팅 히스토리 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 사용자 입력
    if prompt := st.chat_input("질문을 입력하세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI 응답 생성
        with st.chat_message("assistant"):
            with st.spinner("AI 비서가 응답을 생성하는 중..."):
                try:
                    # 간단한 질문인지 복잡한 작업인지 판단
                    if len(prompt) < 100 and not any(keyword in prompt.lower() for keyword in ['분석', '조사', '연구', '작성', '계획', '프로젝트']):
                        response = st.session_state.assistant.simple_chat(prompt)
                    else:
                        response = st.session_state.assistant.process_request(prompt)
                    
                    st.markdown(response)
                    
                    # AI 응답을 메시지 히스토리에 추가
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"오류가 발생했습니다: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # 채팅 히스토리 초기화 버튼
    if st.session_state.messages:
        if st.button("🗑️ 채팅 히스토리 초기화"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()


