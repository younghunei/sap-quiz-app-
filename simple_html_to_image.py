#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import tempfile
import webbrowser
from PIL import ImageGrab
import tkinter as tk
from tkinter import messagebox

def html_to_image(html_content=None, html_file=None, output_image="output.png", wait_time=2):
    """HTML을 이미지로 변환합니다.
    
    Args:
        html_content (str, optional): HTML 문자열 내용. 기본값은 None.
        html_file (str, optional): HTML 파일 경로. 기본값은 None.
        output_image (str, optional): 출력 이미지 파일 경로. 기본값은 "output.png".
        wait_time (int, optional): 브라우저가 로드될 때까지 기다리는 시간(초). 기본값은 2.
    
    Returns:
        str: 생성된 이미지 파일 경로
    """
    # 임시 HTML 파일 생성
    if html_content:
        # HTML 문자열에서 임시 파일 생성
        with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            temp_html_path = f.name
    elif html_file:
        # 이미 존재하는 HTML 파일 사용
        temp_html_path = os.path.abspath(html_file)
    else:
        raise ValueError("HTML 내용이나 파일 경로를 제공해야 합니다.")
    
    # 파일 URL 생성
    file_url = f'file://{temp_html_path}'
    
    # 메시지 창 생성을 위한 루트 윈도우
    root = tk.Tk()
    root.withdraw()  # 루트 윈도우 숨기기
    
    # 사용자에게 지시사항 안내
    messagebox.showinfo("HTML을 이미지로 변환", 
                       f"브라우저가 곧 열립니다. 페이지가 로드되면 스크린샷을 캡처할 준비가 되었을 때 '확인'을 클릭하세요.")
    
    # 브라우저 열기
    webbrowser.open(file_url)
    
    # 페이지가 로드될 때까지 대기
    time.sleep(wait_time)
    
    # 사용자에게 스크린샷 준비 알림
    result = messagebox.askokcancel("스크린샷 준비", 
                                   "브라우저 창이 완전히 보이고 내용이 모두 로드되었으면 '확인'을 클릭하세요.\n"
                                   "스크린샷을 캡처합니다.")
    
    if result:
        # 잠시 대기하여 대화상자가 사라지게 함
        time.sleep(0.5)
        
        # 스크린샷 캡처
        screenshot = ImageGrab.grab()
        
        # 이미지 저장
        screenshot.save(output_image)
        
        # 임시 파일 삭제 (직접 제공한 파일이 아닌 경우에만)
        if html_content:
            os.unlink(temp_html_path)
        
        # 완료 메시지
        messagebox.showinfo("변환 완료", f"이미지가 '{output_image}'에 저장되었습니다.")
        
        return output_image
    else:
        # 사용자가 캡처를 취소한 경우
        if html_content:  # 임시 파일 삭제
            os.unlink(temp_html_path)
        raise Exception("사용자가 스크린샷 캡처를 취소했습니다.")

def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        # 테스트 HTML 콘텐츠
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>테스트</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    background-color: #f5f5f5;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    width: 400px;
                    text-align: center;
                }
                h1 { color: #3498db; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>안녕하세요!</h1>
                <p>이것은 HTML을 이미지로 변환하는 테스트입니다.</p>
                <p>현재 시간: <b id="time"></b></p>
                <script>
                    document.getElementById('time').textContent = new Date().toLocaleString();
                </script>
            </div>
        </body>
        </html>
        """
        
        try:
            # HTML 문자열을 이미지로 변환
            print("HTML 문자열을 이미지로 변환 중...")
            output_path = html_to_image(
                html_content=html_content,
                output_image="test_output.png",
                wait_time=2
            )
            print(f"이미지가 성공적으로 생성되었습니다: {output_path}")
            
        except Exception as e:
            print(f"오류 발생: {e}")
    else:
        # 명령줄 인수로 HTML 파일 경로를 받음
        html_file = sys.argv[1]
        output = "output.png" if len(sys.argv) < 3 else sys.argv[2]
        
        try:
            print(f"HTML 파일 '{html_file}'을 이미지로 변환 중...")
            output_path = html_to_image(
                html_file=html_file,
                output_image=output,
                wait_time=2
            )
            print(f"이미지가 성공적으로 생성되었습니다: {output_path}")
            
        except Exception as e:
            print(f"오류 발생: {e}")

if __name__ == "__main__":
    main() 