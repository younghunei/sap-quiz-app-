import streamlit as st
import json
import random
import pandas as pd
import os

# 페이지 기본 설정
st.set_page_config(
    page_title="SAP 문제 풀이 앱",
    page_icon="📚",
    layout="centered"
)

# 스타일 설정
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .question-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
    }
    .option-box {
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 0.5rem;
    }
    .option-box:hover {
        background-color: #e9ecef;
    }
    .correct {
        background-color: #d4edda;
    }
    .incorrect {
        background-color: #f8d7da;
    }
    .result-box {
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        margin-top: 1rem;
    }
    .result-correct {
        background-color: #d4edda;
        color: #155724;
    }
    .result-incorrect {
        background-color: #f8d7da;
        color: #721c24;
    }
    .smaller-question {
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# 문제 데이터 로드 함수
@st.cache_data
def load_questions():
    try:
        with open('questions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"문제 데이터를 불러오는 데 실패했습니다: {e}")
        return []

# 문제 셔플 함수
def shuffle_questions(questions):
    shuffled = questions.copy()
    random.shuffle(shuffled)
    return shuffled

# 세션 상태 초기화
if 'questions' not in st.session_state:
    st.session_state.questions = load_questions()
    
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
    
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
    
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
    
if 'score' not in st.session_state:
    st.session_state.score = 0
    
if 'shuffled' not in st.session_state:
    st.session_state.shuffled = False

# 사용자 응답 처리 함수
def handle_answer(question_number, selected_option):
    st.session_state.user_answers[question_number] = selected_option
    if st.session_state.current_question_index < len(st.session_state.questions) - 1:
        st.session_state.current_question_index += 1
    else:
        calculate_score()
        st.session_state.show_result = True

# 점수 계산 함수
def calculate_score():
    correct_count = 0
    for q_num, answer in st.session_state.user_answers.items():
        correct_answer = next((q['answer'] for q in st.session_state.questions if q['number'] == q_num), None)
        if answer == correct_answer:
            correct_count += 1
    
    st.session_state.score = correct_count
    return correct_count

# 퀴즈 재시작 함수
def restart_quiz():
    st.session_state.current_question_index = 0
    st.session_state.user_answers = {}
    st.session_state.show_result = False
    st.session_state.score = 0

# 문제 섞기 함수
def shuffle_and_restart():
    st.session_state.questions = shuffle_questions(st.session_state.questions)
    st.session_state.shuffled = True
    restart_quiz()

# 메인 앱 UI - 시작 페이지
st.title("📚 SAP 문제 풀이 앱")

st.markdown("""
### 환영합니다!

이 앱은 SAP 관련 문제를 풀 수 있는 학습 도구입니다. 
다음과 같은 기능을 제공합니다:

- **일반 학습 모드**: 문제에 답변 후 바로 정답과 설명을 확인할 수 있습니다.
- **시험 모드**: 모든 문제를 푼 후 결과를 확인할 수 있습니다.

왼쪽 사이드바에서 원하는 기능을 선택하세요.
""")

# 문제 통계 표시
questions = load_questions()
st.write(f"### 총 {len(questions)}개의 문제가 준비되어 있습니다.")

# 시작하기 버튼들
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 학습 모드")
    st.write("문제 풀이 후 바로 정답을 확인할 수 있습니다.")
    st.page_link("pages/learning_mode.py", label="학습 모드 시작하기", icon="🎓")

with col2:
    st.markdown("#### 시험 모드")
    st.write("모든 문제를 풀고 난 후 결과를 확인합니다.")
    st.page_link("pages/exam_mode.py", label="시험 모드 시작하기", icon="📝")

# 푸터
st.divider()