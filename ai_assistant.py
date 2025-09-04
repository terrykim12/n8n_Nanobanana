import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# 환경 변수 로드
load_dotenv()

class AIAssistant:
    def __init__(self):
        """AI 비서 초기화"""
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # 에이전트들 생성
        self.agents = self._create_agents()
        
    def _create_agents(self) -> Dict[str, Agent]:
        """AI 에이전트들을 생성합니다."""
        agents = {}
        
        # 메인 비서 에이전트
        agents['assistant'] = Agent(
            role='AI 비서',
            goal='사용자의 요청을 이해하고 적절한 도움을 제공합니다',
            backstory="""당신은 친근하고 도움이 되는 AI 비서입니다. 
            사용자의 질문에 정확하고 유용한 답변을 제공하며, 
            필요시 다른 전문가 에이전트들과 협력하여 작업을 수행합니다.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
        
        # 연구원 에이전트
        agents['researcher'] = Agent(
            role='연구원',
            goal='정확하고 최신의 정보를 수집하고 분석합니다',
            backstory="""당신은 정보 수집과 분석에 특화된 연구원입니다. 
            다양한 소스에서 신뢰할 수 있는 정보를 찾아내고, 
            복잡한 주제를 이해하기 쉽게 정리합니다.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
        
        # 작성자 에이전트
        agents['writer'] = Agent(
            role='작성자',
            goal='수집된 정보를 바탕으로 명확하고 매력적인 콘텐츠를 작성합니다',
            backstory="""당신은 창의적이고 명확한 글쓰기 능력을 가진 작성자입니다. 
            복잡한 정보를 이해하기 쉽게 정리하고, 
            사용자가 원하는 형식에 맞춰 콘텐츠를 작성합니다.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
        
        # 분석가 에이전트
        agents['analyst'] = Agent(
            role='데이터 분석가',
            goal='데이터를 분석하고 인사이트를 도출합니다',
            backstory="""당신은 데이터 분석과 해석에 전문성을 가진 분석가입니다. 
            다양한 데이터를 분석하여 의미 있는 패턴을 찾아내고, 
            실용적인 권장사항을 제시합니다.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
        
        return agents
    
    def create_task(self, description: str, agent_role: str, expected_output: str = "") -> Task:
        """작업을 생성합니다."""
        return Task(
            description=description,
            agent=self.agents[agent_role],
            expected_output=expected_output
        )
    
    def process_request(self, user_request: str) -> str:
        """사용자 요청을 처리합니다."""
        try:
            # 요청 분석 작업
            analysis_task = self.create_task(
                description=f"사용자의 요청을 분석하고 어떤 작업이 필요한지 파악하세요: {user_request}",
                agent_role='assistant',
                expected_output="요청 분석 결과와 필요한 작업 단계"
            )
            
            # 정보 수집 작업
            research_task = self.create_task(
                description="분석 결과를 바탕으로 필요한 정보를 수집하고 조사하세요",
                agent_role='researcher',
                expected_output="수집된 정보와 출처"
            )
            
            # 분석 작업
            analysis_task2 = self.create_task(
                description="수집된 정보를 분석하고 인사이트를 도출하세요",
                agent_role='analyst',
                expected_output="분석 결과와 주요 인사이트"
            )
            
            # 최종 응답 작성 작업
            writing_task = self.create_task(
                description="모든 정보를 종합하여 사용자에게 명확하고 유용한 응답을 작성하세요",
                agent_role='writer',
                expected_output="사용자 요청에 대한 최종 응답"
            )
            
            # 작업 순서 정의
            analysis_task >> research_task >> analysis_task2 >> writing_task
            
            # Crew 생성 및 실행
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=[analysis_task, research_task, analysis_task2, writing_task],
                verbose=True,
                process=Process.sequential
            )
            
            # 작업 실행
            result = crew.kickoff()
            
            return result
            
        except Exception as e:
            return f"오류가 발생했습니다: {str(e)}"
    
    def simple_chat(self, message: str) -> str:
        """간단한 채팅 응답을 생성합니다."""
        try:
            task = self.create_task(
                description=f"사용자의 메시지에 대해 친근하고 도움이 되는 응답을 작성하세요: {message}",
                agent_role='assistant',
                expected_output="친근하고 도움이 되는 응답"
            )
            
            crew = Crew(
                agents=[self.agents['assistant']],
                tasks=[task],
                verbose=False
            )
            
            result = crew.kickoff()
            return result
            
        except Exception as e:
            return f"오류가 발생했습니다: {str(e)}"

def main():
    """메인 함수"""
    print("AI 비서를 초기화하는 중...")
    
    # OpenAI API 키 확인
    if not os.getenv("OPENAI_API_KEY"):
        print("오류: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("env_example.txt 파일을 참고하여 .env 파일을 생성하고 API 키를 설정하세요.")
        return
    
    # AI 비서 생성
    assistant = AIAssistant()
    
    print("AI 비서가 준비되었습니다!")
    print("종료하려면 'quit' 또는 'exit'를 입력하세요.")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("사용자: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '종료']:
                print("AI 비서를 종료합니다. 안녕히 가세요!")
                break
            
            if not user_input:
                continue
            
            print("\nAI 비서가 응답을 생성하는 중...")
            
            # 간단한 채팅인지 복잡한 작업인지 판단
            if len(user_input) < 100 and not any(keyword in user_input.lower() for keyword in ['분석', '조사', '연구', '작성', '계획']):
                response = assistant.simple_chat(user_input)
            else:
                response = assistant.process_request(user_input)
            
            print(f"\nAI 비서: {response}\n")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\nAI 비서를 종료합니다. 안녕히 가세요!")
            break
        except Exception as e:
            print(f"\n오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()


