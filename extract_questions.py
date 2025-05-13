import PyPDF2
import re
import json
import os

def extract_questions_from_pdf(pdf_path):
    """
    PDF 파일에서 문제와 정답을 추출합니다.
    
    실제 PDF 구조에 따라 이 함수를 수정해야 할 수 있습니다.
    현재는 일반적인 패턴을 가정하고 있습니다.
    """
    questions = []
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            full_text = ""
            
            # PDF의 모든 페이지 텍스트 추출
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                full_text += page.extract_text()
            
            # 문제와 정답을 추출하는 패턴
            # 아래 패턴은 예시입니다. PDF 구조에 맞게 수정이 필요합니다.
            # 예: "1. 문제내용\nA) 선택지1\nB) 선택지2\nC) 선택지3\nD) 선택지4\n정답: B"
            pattern = r'(\d+)\.\s+(.*?)(?:\n[A-D]\)\s+.*?){2,4}\n정답:\s+([A-D])'
            matches = re.finditer(pattern, full_text, re.DOTALL)
            
            for match in matches:
                q_num = match.group(1)
                q_text = match.group(2).strip()
                answer = match.group(3).strip()
                
                # 선택지 추출
                options_pattern = r'([A-D]\))\s+(.*?)(?=\n[A-D]\)|$|\n정답:)'
                options_matches = re.finditer(options_pattern, match.group(0), re.DOTALL)
                options = {}
                
                for opt_match in options_matches:
                    opt_letter = opt_match.group(1).replace(')', '')
                    opt_text = opt_match.group(2).strip()
                    options[opt_letter] = opt_text
                
                question = {
                    "number": q_num,
                    "question": q_text,
                    "options": options,
                    "answer": answer
                }
                questions.append(question)
        
        return questions
    
    except Exception as e:
        print(f"PDF 처리 중 오류 발생: {e}")
        return []

def save_questions_to_json(questions, output_file="questions.json"):
    """
    추출된 문제와 정답을 JSON 파일로 저장합니다.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)
    
    print(f"{len(questions)}개 문제가 {output_file}에 저장되었습니다.")

if __name__ == "__main__":
    pdf_path = "Sap 한글.pdf"
    
    if os.path.exists(pdf_path):
        questions = extract_questions_from_pdf(pdf_path)
        if questions:
            save_questions_to_json(questions)
        else:
            print("PDF에서 문제를 추출할 수 없습니다. 패턴을 수정해보세요.")
    else:
        print(f"PDF 파일을 찾을 수 없습니다: {pdf_path}") 