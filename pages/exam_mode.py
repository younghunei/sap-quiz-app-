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
    
if 'selected_question_numbers' not in st.session_state:
    st.session_state.selected_question_numbers = []
    
if 'filtered_exam_questions' not in st.session_state:
    st.session_state.filtered_exam_questions = []
    
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

# 선택된 문제들로 필터링하는 함수 수정 - 안전한 타입 변환
def filter_questions_by_selection():
    if st.session_state.selected_question_numbers:
        # 선택된 번호와 일치하는 문제들만 필터링 - 안전한 변환
        filtered_questions = []
        for q in st.session_state.exam_questions:
            try:
                # 안전하게 숫자로 변환
                question_num = q.get('number', '')
                if question_num and str(question_num).strip():  # 빈 값이 아닌지 확인
                    num = int(str(question_num).strip())
                    if num in st.session_state.selected_question_numbers:
                        filtered_questions.append(q)
            except (ValueError, TypeError):
                # 변환할 수 없는 값은 무시
                continue
        
        st.session_state.filtered_exam_questions = filtered_questions
        print(f"Debug: 선택된 번호: {st.session_state.selected_question_numbers}")
        print(f"Debug: 필터링된 문제 수: {len(st.session_state.filtered_exam_questions)}")
    else:
        st.session_state.filtered_exam_questions = []

# 선택된 문제들로 시험 시작하는 함수 수정
def start_selected_exam():
    print(f"Debug: 시험 시작 함수 호출됨")
    print(f"Debug: 선택된 문제 번호: {st.session_state.selected_question_numbers}")
    
    filter_questions_by_selection()
    
    print(f"Debug: 필터링 후 문제 수: {len(st.session_state.filtered_exam_questions)}")
    
    if st.session_state.filtered_exam_questions:
        st.session_state.current_exam_index = 0
        st.session_state.exam_user_answers = {}
        st.session_state.show_exam_result = False
        st.session_state.exam_score = 0
        st.toast(f"{len(st.session_state.filtered_exam_questions)}개 문제로 시험을 시작합니다!", icon="🎯")
        print(f"Debug: 시험 시작 성공!")
    else:
        st.toast("문제를 선택해주세요!", icon="⚠️")
        print(f"Debug: 필터링된 문제가 없음")

# 사용자 응답 처리 함수 (수정)
def handle_exam_answer(question_number, selected_options):
    st.session_state.exam_user_answers[question_number] = selected_options
    if st.session_state.current_exam_index < len(st.session_state.filtered_exam_questions) - 1:
        st.session_state.current_exam_index += 1
    else:
        calculate_exam_score()
        st.session_state.show_exam_result = True

# 점수 계산 함수 (수정)
def calculate_exam_score():
    correct_count = 0
    for q_num, answers in st.session_state.exam_user_answers.items():
        correct_answer = next((q['answer'] for q in st.session_state.filtered_exam_questions if q['number'] == q_num), None)
        
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

# 퀴즈 재시작 함수 (수정)
def restart_exam():
    st.session_state.current_exam_index = 0
    st.session_state.exam_user_answers = {}
    st.session_state.show_exam_result = False
    st.session_state.exam_score = 0

# 문제 섞기 함수 (수정)
def shuffle_and_restart_exam():
    if st.session_state.filtered_exam_questions:
        st.session_state.filtered_exam_questions = shuffle_questions(st.session_state.filtered_exam_questions)
        st.session_state.exam_shuffled = True
        restart_exam()

# 범위 문자열 파싱 함수 추가 (기존 함수들 다음에 추가)
def parse_question_numbers(input_text):
    """
    입력 문자열을 파싱하여 문제 번호 리스트 반환
    예시: 
    - "1,2,3,5" -> [1, 2, 3, 5]
    - "1~10" -> [1, 2, 3, ..., 10]
    - "1,5~8,12" -> [1, 5, 6, 7, 8, 12]
    """
    try:
        numbers = []
        input_text = input_text.strip()
        
        # 쉼표로 구분된 각 부분 처리
        parts = input_text.split(',')
        
        for part in parts:
            part = part.strip()
            if '~' in part or '-' in part:
                # 범위 처리
                separator = '~' if '~' in part else '-'
                start, end = part.split(separator)
                start_num = int(start.strip())
                end_num = int(end.strip())
                numbers.extend(list(range(start_num, end_num + 1)))
            else:
                # 단일 번호
                numbers.append(int(part))
        
        # 중복 제거 및 정렬
        return sorted(list(set(numbers)))
    except (ValueError, AttributeError):
        return []

# 메인 앱 UI - 시험 모드
st.title("📝 시험 모드")

# 사이드바
with st.sidebar:
    st.header("문제 선택")
    
    # 전체 문제 정보
    all_questions = load_questions()
    if all_questions:
        # number 필드를 안전하게 정수로 변환
        available_numbers = []
        for q in all_questions:
            try:
                question_num = q.get('number', '')
                if question_num and str(question_num).strip():  # 빈 값이 아닌지 확인
                    num = int(str(question_num).strip())
                    available_numbers.append(num)
            except (ValueError, TypeError):
                # 변환할 수 없는 값은 무시하고 계속 진행
                continue
        
        if available_numbers:
            available_numbers.sort()  # 정렬
            min_num = min(available_numbers)
            max_num = max(available_numbers)
            st.info(f"총 {len(available_numbers)}개 문제 (문제 {min_num}번 ~ {max_num}번)")
        else:
            available_numbers = []
            st.warning("유효한 문제 번호를 찾을 수 없습니다.")
    else:
        available_numbers = []
        st.warning("문제 데이터를 불러올 수 없습니다.")
    
    # 직접 문제 번호 입력 섹션
    st.subheader("🎯 문제 번호 직접 입력")
    
    # 입력 예시 표시
    with st.expander("📝 입력 방법 안내", expanded=False):
        st.markdown("""
        **입력 방법:**
        - **개별 번호**: `1,5,10,15` (쉼표로 구분)
        - **범위**: `1~10` 또는 `1-10` (1번부터 10번까지)
        - **혼합**: `1,5~8,12,20~25` (개별 번호와 범위 혼합)
        
        **예시:**
        - `1,2,3,5`: 1, 2, 3, 5번 문제
        - `1~50`: 1번부터 50번까지
        - `1~10,20~30,45`: 1-10번, 20-30번, 45번 문제
        """)
    
    # 문제 번호 입력 필드
    question_input = st.text_area(
        "문제 번호 입력:",
        placeholder="예: 1,5~10,15,20~25",
        help="쉼표(,)로 구분하여 입력하세요. 범위는 ~나 -로 표시",
        height=100,
        key="question_numbers_input"
    )
    
    # 입력된 번호 적용 버튼
    if st.button("📋 입력한 번호로 선택", use_container_width=True, key="apply_input_numbers"):
        if question_input.strip():
            parsed_numbers = parse_question_numbers(question_input)
            if parsed_numbers:
                # 실제 존재하는 문제만 필터링
                valid_numbers = [num for num in parsed_numbers if num in available_numbers]
                invalid_numbers = [num for num in parsed_numbers if num not in available_numbers]
                
                st.session_state.selected_question_numbers = valid_numbers
                
                if valid_numbers:
                    st.toast(f"✅ {len(valid_numbers)}개 문제가 선택되었습니다!", icon="✅")
                    if invalid_numbers:
                        st.warning(f"⚠️ 존재하지 않는 문제 번호: {', '.join(map(str, invalid_numbers))}")
                    st.rerun()
                else:
                    st.toast("❌ 유효한 문제가 없습니다!", icon="❌")
            else:
                st.toast("❌ 올바른 형식으로 입력해주세요!", icon="❌")
        else:
            st.toast("❌ 문제 번호를 입력해주세요!", icon="❌")
    
    # 입력 미리보기
    if question_input.strip():
        preview_numbers = parse_question_numbers(question_input)
        if preview_numbers:
            valid_preview = [num for num in preview_numbers if num in available_numbers]
            invalid_preview = [num for num in preview_numbers if num not in available_numbers]
            
            st.write("**입력 미리보기:**")
            if valid_preview:
                # 연속된 번호들을 범위로 표시
                ranges = []
                start = valid_preview[0]
                end = valid_preview[0]
                
                for i in range(1, len(valid_preview)):
                    if valid_preview[i] == end + 1:
                        end = valid_preview[i]
                    else:
                        if start == end:
                            ranges.append(str(start))
                        else:
                            ranges.append(f"{start}~{end}")
                        start = end = valid_preview[i]
                
                # 마지막 범위 추가
                if start == end:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}~{end}")
                
                st.success(f"✅ 유효한 문제: {len(valid_preview)}개 ({', '.join(ranges)})")
            
            if invalid_preview:
                st.error(f"❌ 존재하지 않는 문제: {', '.join(map(str, invalid_preview))}")
    
    st.divider()
    
    # 전체 선택/해제 버튼
    col1, col2 = st.columns(2)
    with col1:
        if st.button("전체 선택", use_container_width=True, key="select_all"):
            st.session_state.selected_question_numbers = available_numbers.copy()
            st.rerun()
    
    with col2:
        if st.button("전체 해제", use_container_width=True, key="deselect_all"):
            st.session_state.selected_question_numbers = []
            st.rerun()
    
    st.divider()
    
    # 현재 선택 상태 표시 및 시험 시작 버튼
    if st.session_state.selected_question_numbers:
        sorted_numbers = sorted(st.session_state.selected_question_numbers)
        
        # 연속된 번호들을 범위로 표시
        ranges = []
        start = sorted_numbers[0]
        end = sorted_numbers[0]
        
        for i in range(1, len(sorted_numbers)):
            if sorted_numbers[i] == end + 1:
                end = sorted_numbers[i]
            else:
                if start == end:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}~{end}")
                start = end = sorted_numbers[i]
        
        # 마지막 범위 추가
        if start == end:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}~{end}")
        
        st.success(f"**선택된 문제: {len(sorted_numbers)}개**")
        st.write(f"**범위:** {', '.join(ranges)}")
        
        # 시험 시작 버튼 - 더 눈에 띄게
        st.markdown("---")
        if st.button("🚀 시험 시작", type="primary", use_container_width=True, key="start_exam_btn"):
            st.write(f"선택된 문제 번호: {st.session_state.selected_question_numbers}")
            st.write(f"전체 문제 수: {len(st.session_state.exam_questions)}")
            
            # 필터링 테스트 - 안전한 변환
            test_filtered = []
            for q in st.session_state.exam_questions:
                try:
                    question_num = q.get('number', '')
                    if question_num and str(question_num).strip():
                        num = int(str(question_num).strip())
                        if num in st.session_state.selected_question_numbers:
                            test_filtered.append(q)
                except (ValueError, TypeError):
                    continue
            
            st.write(f"필터링될 문제 수: {len(test_filtered)}")
            
            start_selected_exam()
            st.rerun()
        
        # 선택 초기화 버튼
        if st.button("🗑️ 선택 초기화", use_container_width=True, key="clear_selection"):
            st.session_state.selected_question_numbers = []
            st.rerun()
    else:
        st.info("위에서 문제 번호를 입력하고 '📋 입력한 번호로 선택' 버튼을 클릭하세요.")
        
        # 빠른 예시 버튼들 추가
        st.markdown("### ⚡ 빠른 예시")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("처음 50문제", use_container_width=True, key="quick_50"):
                valid_numbers = [num for num in range(1, 51) if num in available_numbers]
                st.session_state.selected_question_numbers = valid_numbers
                st.toast(f"처음 50문제: {len(valid_numbers)}개 문제가 선택되었습니다!", icon="✅")
                st.rerun()
        
        with col2:
            if st.button("전체 문제", use_container_width=True, key="quick_all"):
                st.session_state.selected_question_numbers = available_numbers.copy()
                st.toast(f"전체 문제: {len(available_numbers)}개 문제가 선택되었습니다!", icon="✅")
                st.rerun()
    
    st.divider()
    st.header("옵션")
    
    if st.button("문제 섞기", key="shuffle_btn"):
        shuffle_and_restart_exam()
    
    if st.button("문제 순서 초기화", key="reset_order_btn"):
        st.session_state.exam_questions = load_questions()
        st.session_state.exam_shuffled = False
        restart_exam()
    
    if st.button("시험 재시작", key="restart_exam_btn"):
        restart_exam()
    
    st.divider()
    st.write("### 현재 상태")
    if st.session_state.filtered_exam_questions:
        st.write(f"시험 문제 수: {len(st.session_state.filtered_exam_questions)}")
        st.write(f"현재 문제: {st.session_state.current_exam_index + 1}")
        st.write(f"답변한 문제: {len(st.session_state.exam_user_answers)}")
    else:
        st.write("시험이 시작되지 않았습니다.")
    st.write(f"문제 섞기: {'활성화됨' if st.session_state.exam_shuffled else '비활성화됨'}")
    
    st.divider()
    if st.button("메인 페이지로 돌아가기", key="go_home_btn"):
        st.switch_page("app.py")

# 결과 화면 (수정)
if st.session_state.show_exam_result:
    st.header("시험 결과")
    
    total_questions = len(st.session_state.filtered_exam_questions)
    correct_count = st.session_state.exam_score
    
    st.write(f"총 {total_questions}문제 중 {correct_count}문제 정답!")
    st.progress(correct_count / total_questions)
    
    st.write(f"점수: {int((correct_count / total_questions) * 100)}점")
    
    for q in st.session_state.filtered_exam_questions:
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

# 문제 화면 (수정)
else:
    if not st.session_state.filtered_exam_questions:
        st.info("🎯 왼쪽 사이드바에서 문제를 선택하고 '🚀 시험 시작' 버튼을 클릭하세요!")
        
        # 중앙에 큰 안내 메시지
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px; margin: 2rem 0;">
            <h3>📚 시험 모드 사용법</h3>
            <p><strong>문제 번호 직접 입력:</strong> 원하는 문제 번호를 직접 입력</p>
            <p><strong>범위 선택:</strong> 시작/끝 번호 입력 후 적용</p>
            <p><strong>시험 시작:</strong> '🚀 시험 시작' 버튼 클릭</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 예시 표시
        st.markdown("""
        ### 📝 입력 예시
        - **개별 문제**: `1,5,10,15` (1, 5, 10, 15번 문제)
        - **범위**: `1~50` (1번부터 50번까지)
        - **혼합**: `1~10,20,30~35` (1-10번, 20번, 30-35번 문제)
        """)
    else:
        current_q = st.session_state.filtered_exam_questions[st.session_state.current_exam_index]
        question_number = current_q['number']
        correct_answer = current_q['answer']
        
        # 정답이 다중 선택인지 확인
        is_multiple_choice = ',' in correct_answer
        
        st.header(f"문제 {st.session_state.current_exam_index + 1}/{len(st.session_state.filtered_exam_questions)}")
        
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
        st.progress((st.session_state.current_exam_index) / len(st.session_state.filtered_exam_questions))
        
        # 답변 상태 표시
        answered_count = len(st.session_state.exam_user_answers)
        st.write(f"답변한 문제: {answered_count}/{len(st.session_state.filtered_exam_questions)}")

# 푸터
st.divider()
st.markdown("SAP 문제 풀이 앱 - 시험 모드")

# 디버깅을 위한 코드 추가
if st.button("🔍 데이터 확인", key="debug_data"):
    st.write("첫 번째 문제 데이터:")
    if st.session_state.exam_questions:
        first_q = st.session_state.exam_questions[0]
        st.write(first_q)
        st.write(f"number 필드 타입: {type(first_q.get('number'))}")
        st.write(f"number 필드 값: '{first_q.get('number')}'")