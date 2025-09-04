#!/usr/bin/env python3
"""
AI 비서 사용 예시
이 파일은 AI 비서의 다양한 기능을 테스트하고 사용법을 보여줍니다.
"""

import os
from dotenv import load_dotenv
from ai_assistant import AIAssistant

def test_simple_chat():
    """간단한 채팅 테스트"""
    print("=== 간단한 채팅 테스트 ===")
    
    # 간단한 질문들
    simple_questions = [
        "안녕하세요!",
        "오늘 날씨는 어때요?",
        "파이썬이란 무엇인가요?",
        "감사합니다!"
    ]
    
    for question in simple_questions:
        print(f"\n사용자: {question}")
        response = assistant.simple_chat(question)
        print(f"AI 비서: {response}")
        print("-" * 50)

def test_complex_tasks():
    """복잡한 작업 테스트"""
    print("\n=== 복잡한 작업 테스트 ===")
    
    # 복잡한 작업들
    complex_tasks = [
        "2024년 AI 기술 트렌드를 분석해주세요",
        "새로운 웹 애플리케이션 개발 프로젝트 계획을 수립해주세요",
        "마케팅 전략을 연구하고 제안해주세요"
    ]
    
    for task in complex_tasks:
        print(f"\n사용자: {task}")
        print("AI 비서가 여러 에이전트와 협력하여 작업을 수행합니다...")
        response = assistant.process_request(task)
        print(f"AI 비서: {response}")
        print("=" * 80)

def test_custom_scenarios():
    """사용자 정의 시나리오 테스트"""
    print("\n=== 사용자 정의 시나리오 테스트 ===")
    
    # 사용자가 직접 입력할 수 있는 인터페이스
    print("직접 질문을 입력해보세요 (종료하려면 'quit' 입력):")
    
    while True:
        try:
            user_input = input("\n사용자: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '종료']:
                print("테스트를 종료합니다.")
                break
            
            if not user_input:
                continue
            
            print("AI 비서가 응답을 생성하는 중...")
            
            # 간단한 질문인지 복잡한 작업인지 판단
            if len(user_input) < 100 and not any(keyword in user_input.lower() for keyword in ['분석', '조사', '연구', '작성', '계획', '프로젝트']):
                response = assistant.simple_chat(user_input)
            else:
                response = assistant.process_request(user_input)
            
            print(f"AI 비서: {response}")
            
        except KeyboardInterrupt:
            print("\n\n테스트를 종료합니다.")
            break
        except Exception as e:
            print(f"오류가 발생했습니다: {str(e)}")

def main():
    """메인 함수"""
    global assistant
    
    print("🤖 AI 비서 테스트 프로그램")
    print("=" * 50)
    
    # 환경 변수 로드
    load_dotenv()
    
    # OpenAI API 키 확인
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 오류: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("env_example.txt 파일을 참고하여 .env 파일을 생성하고 API 키를 설정하세요.")
        return
    
    try:
        print("🔄 AI 비서를 초기화하는 중...")
        assistant = AIAssistant()
        print("✅ AI 비서가 성공적으로 초기화되었습니다!")
        
        # 테스트 실행
        test_simple_chat()
        test_complex_tasks()
        test_custom_scenarios()
        
    except Exception as e:
        print(f"❌ AI 비서 초기화 중 오류가 발생했습니다: {str(e)}")
        print("API 키가 올바른지, 인터넷 연결이 안정적인지 확인해주세요.")

if __name__ == "__main__":
    main()


