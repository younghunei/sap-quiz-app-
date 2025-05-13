import streamlit as st
import json
import random
import pandas as pd
import os

# 페이지 기본 설정
st.set_page_config(
    page_title="시험 모드 - SAP 문제 풀이 앱",
    page_icon="📝",
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

# 정답 비교 함수 - 다중 정답 지원
def check_exam_answer(user_answer, correct_answer):
    # 정답이 쉼표로 구분된 여러 답변인 경우 처리
    if ',' in correct_answer:
        correct_options = correct_answer.split(',')
        
        # 사용자 응답이 목록인 경우
        if isinstance(user_answer, list):
            user_options = user_answer
        else:
            user_options = user_answer.split(',')
        
        # 정답 수와 사용자 답변 수가 같은지 확인
        if len(correct_options) != len(user_options):
            return False
        
        # 모든 정답이 사용자 답변에 포함되어 있는지 확인
        for option in correct_options:
            if option.strip() not in [opt.strip() for opt in user_options]:
                return False
        
        return True
    else:
        # 단일 정답인 경우
        if isinstance(user_answer, list):
            return len(user_answer) == 1 and user_answer[0] == correct_answer
        else:
            return user_answer == correct_answer

# 세션 상태 초기화
if 'exam_questions' not in st.session_state:
    st.session_state.exam_questions = load_questions()
    
if 'current_exam_index' not in st.session_state:
    st.session_state.current_exam_index = 0
    
if 'exam_user_answers' not in st.session_state:
    st.session_state.exam_user_answers = {}
    
if 'show_exam_result' not in st.session_state:
    st.session_state.show_exam_result = False
    
if 'exam_score' not in st.session_state:
    st.session_state.exam_score = 0
    
if 'exam_shuffled' not in st.session_state:
    st.session_state.exam_shuffled = False

# 사용자 응답 처리 함수
def handle_exam_answer(question_number, selected_options):
    st.session_state.exam_user_answers[question_number] = selected_options
    if st.session_state.current_exam_index < len(st.session_state.exam_questions) - 1:
        st.session_state.current_exam_index += 1
    else:
        calculate_exam_score()
        st.session_state.show_exam_result = True

# 점수 계산 함수
def calculate_exam_score():
    correct_count = 0
    for q_num, answers in st.session_state.exam_user_answers.items():
        correct_answer = next((q['answer'] for q in st.session_state.exam_questions if q['number'] == q_num), None)
        
        # 다중 정답 지원
        if ',' in correct_answer:
            # 사용자 응답을 정렬하여 비교
            user_sorted = ','.join(sorted(answers))
            correct_sorted = ','.join(sorted(correct_answer.split(',')))
            if user_sorted == correct_sorted:
                correct_count += 1
        else:
            # 단일 정답
            if len(answers) == 1 and answers[0] == correct_answer:
                correct_count += 1
    
    st.session_state.exam_score = correct_count
    return correct_count

# 퀴즈 재시작 함수
def restart_exam():
    st.session_state.current_exam_index = 0
    st.session_state.exam_user_answers = {}
    st.session_state.show_exam_result = False
    st.session_state.exam_score = 0

# 문제 섞기 함수
def shuffle_and_restart_exam():
    st.session_state.exam_questions = shuffle_questions(st.session_state.exam_questions)
    st.session_state.exam_shuffled = True
    restart_exam()

# 메인 앱 UI - 시험 모드
st.title("📝 시험 모드")

# 사이드바
with st.sidebar:
    st.header("옵션")
    if st.button("문제 섞기"):
        shuffle_and_restart_exam()
    
    if st.button("문제 순서 초기화"):
        st.session_state.exam_questions = load_questions()
        st.session_state.exam_shuffled = False
        restart_exam()
    
    if st.button("시험 재시작"):
        restart_exam()
    
    st.divider()
    st.write("### 현재 상태")
    st.write(f"총 문제 수: {len(st.session_state.exam_questions)}")
    st.write(f"현재 문제: {st.session_state.current_exam_index + 1}")
    st.write(f"답변한 문제: {len(st.session_state.exam_user_answers)}")
    st.write(f"문제 섞기: {'활성화됨' if st.session_state.exam_shuffled else '비활성화됨'}")
    
    st.divider()
    if st.button("메인 페이지로 돌아가기"):
        st.switch_page("app.py")

# 결과 화면
if st.session_state.show_exam_result:
    st.header("시험 결과")
    
    total_questions = len(st.session_state.exam_questions)
    correct_count = st.session_state.exam_score
    
    st.write(f"총 {total_questions}문제 중 {correct_count}문제 정답!")
    st.progress(correct_count / total_questions)
    
    st.write(f"점수: {int((correct_count / total_questions) * 100)}점")
    
    for q in st.session_state.exam_questions:
        q_num = q['number']
        user_answers = st.session_state.exam_user_answers.get(q_num, [])
        correct_answer = q['answer']
        
        # 정답 확인
        if ',' in correct_answer:
            # 다중 정답
            user_sorted = ','.join(sorted(user_answers))
            correct_sorted = ','.join(sorted(correct_answer.split(',')))
            is_correct = user_sorted == correct_sorted
        else:
            # 단일 정답
            is_correct = len(user_answers) == 1 and user_answers[0] == correct_answer
        
        with st.expander(f"문제 {q_num}: {q['question']} {'✅' if is_correct else '❌'}"):
            for opt_key, opt_text in q['options'].items():
                if ',' in correct_answer and opt_key in correct_answer.split(','):
                    st.markdown(f"**{opt_key}) {opt_text} ✓ (정답)**")
                elif opt_key == correct_answer:
                    st.markdown(f"**{opt_key}) {opt_text} ✓ (정답)**")
                elif opt_key in user_answers and (opt_key not in correct_answer.split(',') if ',' in correct_answer else opt_key != correct_answer):
                    st.markdown(f"**{opt_key}) {opt_text} ✗ (선택한 답)**")
                else:
                    st.markdown(f"{opt_key}) {opt_text}")
            
            # 선택한 답변 표시
            st.write(f"선택한 답변: {', '.join(user_answers)}")
            st.write(f"정답: {correct_answer}")
    
    if st.button("시험 다시 보기"):
        restart_exam()

# 문제 화면
else:
    if not st.session_state.exam_questions:
        st.warning("문제 데이터를 불러올 수 없습니다.")
    else:
        current_q = st.session_state.exam_questions[st.session_state.current_exam_index]
        question_number = current_q['number']
        correct_answer = current_q['answer']
        
        # 정답이 다중 선택인지 확인
        is_multiple_choice = ',' in correct_answer
        
        st.header(f"문제 {st.session_state.current_exam_index + 1}/{len(st.session_state.exam_questions)}")
        
        if is_multiple_choice:
            st.info(f"이 문제는 다중 선택 문제입니다. {len(correct_answer.split(','))}개의 답을 선택해주세요.")
        
        with st.container(border=True):
            # 질문을 smaller-question 클래스로 감싸서 글자 크기를 줄임
            st.markdown(f"<div class='smaller-question'>{current_q['question']}</div>", unsafe_allow_html=True)
            
            options = current_q['options']
            
            # 다중 선택 지원
            if is_multiple_choice:
                # 체크박스로 다중 선택 지원
                st.write("정답을 모두 선택하세요:")
                selected_options = []
                
                for opt_key, opt_text in options.items():
                    is_selected = st.checkbox(f"{opt_key}) {opt_text}", 
                              key=f"exam_chk_{question_number}_{opt_key}")
                    if is_selected:
                        selected_options.append(opt_key)
                
                # 제출 버튼
                if st.button("정답 제출", key="exam_submit_btn"):
                    if selected_options:
                        handle_exam_answer(question_number, selected_options)
                        st.rerun()
                    else:
                        st.warning("최소한 하나의 답을 선택해주세요.")
            else:
                # 단일 선택
                for opt_key, opt_text in options.items():
                    if st.button(f"{opt_key}) {opt_text}", key=f"exam_opt_{question_number}_{opt_key}"):
                        handle_exam_answer(question_number, [opt_key])
                        st.rerun()
        
        # 진행 상태 표시
        st.progress((st.session_state.current_exam_index) / len(st.session_state.exam_questions))
        
        # 답변 상태 표시
        answered_count = len(st.session_state.exam_user_answers)
        st.write(f"답변한 문제: {answered_count}/{len(st.session_state.exam_questions)}")

# 푸터
st.divider()
st.markdown("SAP 문제 풀이 앱 - 시험 모드") 