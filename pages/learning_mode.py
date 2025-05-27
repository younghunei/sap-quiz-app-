import streamlit as st
import json
import random
import pandas as pd
import os

# 페이지 기본 설정
st.set_page_config(
    page_title="학습 모드 - SAP 문제 풀이 앱",
    page_icon="🎓",
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
def check_answer(user_answer, correct_answer):
    # 정답이 쉼표로 구분된 여러 답변인 경우 처리
    if ',' in correct_answer:
        correct_options = correct_answer.split(',')
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
        return user_answer == correct_answer

# 세션 상태 초기화
if 'learning_questions' not in st.session_state:
    st.session_state.learning_questions = load_questions()
    
if 'current_learning_index' not in st.session_state:
    st.session_state.current_learning_index = 0
    
if 'learning_showed_answer' not in st.session_state:
    st.session_state.learning_showed_answer = False
    
if 'learning_selected_options' not in st.session_state:
    st.session_state.learning_selected_options = {}
    
if 'learning_shuffled' not in st.session_state:
    st.session_state.learning_shuffled = False

# 다음 문제로 이동 함수
def next_question():
    if st.session_state.current_learning_index < len(st.session_state.learning_questions) - 1:
        st.session_state.current_learning_index += 1
        st.session_state.learning_showed_answer = False
        st.session_state.learning_selected_options = {}
    else:
        st.toast("마지막 문제입니다!", icon="🎉")

# 이전 문제로 이동 함수
def prev_question():
    if st.session_state.current_learning_index > 0:
        st.session_state.current_learning_index -= 1
        st.session_state.learning_showed_answer = False
        st.session_state.learning_selected_options = {}
    else:
        st.toast("첫 번째 문제입니다!", icon="ℹ️")

# 문제 섞기 함수
def shuffle_and_restart():
    st.session_state.learning_questions = shuffle_questions(st.session_state.learning_questions)
    st.session_state.learning_shuffled = True
    st.session_state.current_learning_index = 0
    st.session_state.learning_showed_answer = False
    st.session_state.learning_selected_options = {}

# 문제 번호 클릭 시 해당 문제로 이동하는 함수 추가
def go_to_question(index):
    st.session_state.current_learning_index = index
    st.session_state.learning_showed_answer = False
    st.session_state.learning_selected_options = {}

# 메인 앱 UI - 학습 모드
st.title("🎓 학습 모드")

# 사이드바
with st.sidebar:
    st.header("옵션")
    if st.button("문제 섞기"):
        shuffle_and_restart()
    
    if st.button("문제 순서 초기화"):
        st.session_state.learning_questions = load_questions()
        st.session_state.learning_shuffled = False
        st.session_state.current_learning_index = 0
        st.session_state.learning_showed_answer = False
        st.session_state.learning_selected_options = {}
    
    # 문제 번호 목록 추가
    st.divider()
    st.write("### 문제 목록")
    
    # 스크롤 가능한 컨테이너 내에 문제 번호 나열
    with st.container(height=300):
        for i, q in enumerate(st.session_state.learning_questions):
            # 현재 문제에 표시 추가
            if i == st.session_state.current_learning_index:
                button_label = f"➡️ 문제 {i+1} (현재)"
                button_type = "primary"
            else:
                button_label = f"문제 {i+1}"
                button_type = "secondary"
            
            # 문제 번호 버튼
            st.button(
                button_label, 
                key=f"q_nav_{i}", 
                on_click=go_to_question, 
                args=(i,),
                type=button_type,
                use_container_width=True
            )
    
    st.divider()
    st.write("### 현재 상태")
    st.write(f"총 문제 수: {len(st.session_state.learning_questions)}")
    st.write(f"현재 문제: {st.session_state.current_learning_index + 1}")
    st.write(f"문제 섞기: {'활성화됨' if st.session_state.learning_shuffled else '비활성화됨'}")
    
    st.divider()
    if st.button("메인 페이지로 돌아가기"):
        st.switch_page("app.py")

# 문제 화면
if not st.session_state.learning_questions:
    st.warning("문제 데이터를 불러올 수 없습니다.")
else:
    current_q = st.session_state.learning_questions[st.session_state.current_learning_index]
    question_number = current_q['number']
    correct_answer = current_q['answer']
    
    # 정답이 다중 선택인지 확인
    is_multiple_choice = ',' in correct_answer
    
    st.header(f"문제 {st.session_state.current_learning_index + 1}/{len(st.session_state.learning_questions)}")
    
    if is_multiple_choice:
        st.info(f"이 문제는 다중 선택 문제입니다. {len(correct_answer.split(','))}개의 답을 선택해주세요.")
    
    with st.container(border=True):
        # 질문을 smaller-question 클래스로 감싸서 글자 크기를 줄임
        st.markdown(f"<div class='smaller-question'>{current_q['question']}</div>", unsafe_allow_html=True)
        
        options = current_q['options']
        
        # 선택지 표시 - 다중 선택 지원
        if not st.session_state.learning_showed_answer:
            if is_multiple_choice:
                # 체크박스로 다중 선택 지원
                st.write("정답을 모두 선택하세요:")
                selected_options = []
                
                for opt_key, opt_text in options.items():
                    is_selected = st.checkbox(f"{opt_key}) {opt_text}", 
                                key=f"learning_chk_{question_number}_{opt_key}")
                    if is_selected:
                        selected_options.append(opt_key)
                
                st.session_state.learning_selected_options = selected_options
                
                # 제출 버튼
                if st.button("정답 제출", key="submit_answer_btn"):
                    if selected_options:
                        st.session_state.learning_showed_answer = True
                        st.rerun()
                    else:
                        st.warning("최소한 하나의 답을 선택해주세요.")
            else:
                # 단일 선택 - 기존 방식 유지
                for opt_key, opt_text in options.items():
                    if st.button(f"{opt_key}) {opt_text}", 
                                key=f"learning_opt_{question_number}_{opt_key}"):
                        st.session_state.learning_selected_options = [opt_key]
                        st.session_state.learning_showed_answer = True
                        st.rerun()
        
        # 정답 표시
        if st.session_state.learning_showed_answer:
            st.divider()
            selected_options = st.session_state.learning_selected_options
            
            # 다중 선택 정답 처리
            if is_multiple_choice:
                # 사용자 선택을 정렬된 문자열로 변환
                user_answer = ','.join(sorted(selected_options))
                # 정답도 정렬된 문자열로 변환
                correct_sorted = ','.join(sorted(correct_answer.split(',')))
                
                is_correct = user_answer == correct_sorted
                
                if is_correct:
                    st.success(f"🎉 정답입니다! 선택한 답: {', '.join(selected_options)}")
                else:
                    st.error(f"❌ 오답입니다. 선택한 답: {', '.join(selected_options)}, 정답: {correct_answer}")
            else:
                # 단일 선택 정답 처리
                selected_option = selected_options[0] if selected_options else ""
                is_correct = selected_option == correct_answer
                
                if is_correct:
                    st.success(f"🎉 정답입니다! 선택한 답: {selected_option}")
                else:
                    st.error(f"❌ 오답입니다. 선택한 답: {selected_option}, 정답: {correct_answer}")
            
            # 정답 설명 표시
            st.markdown("### 정답 해설")
            st.markdown("#### 정답: " + correct_answer)
            
            # 선택지 표시 (정답 표시)
            for opt_key, opt_text in options.items():
                if ',' in correct_answer and opt_key in correct_answer.split(','):
                    st.markdown(f"**{opt_key}) {opt_text} ✓ (정답)**")
                elif opt_key == correct_answer:
                    st.markdown(f"**{opt_key}) {opt_text} ✓ (정답)**")
                elif opt_key in selected_options and (opt_key not in correct_answer.split(',') if ',' in correct_answer else opt_key != correct_answer):
                    st.markdown(f"**{opt_key}) {opt_text} ✗ (선택한 답)**")
                else:
                    st.markdown(f"{opt_key}) {opt_text}")
    
    # 진행 상태 표시
    st.progress((st.session_state.current_learning_index) / len(st.session_state.learning_questions))
    
    # 이전/다음 버튼
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 이전 문제", key="prev_btn"):
            prev_question()
            st.rerun()
    
    with col2:
        if st.button("다음 문제 →", key="next_btn"):
            next_question()
            st.rerun()

# 푸터
st.divider()
st.markdown("SAP 문제 풀이 앱 - 학습 모드") 