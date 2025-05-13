#!/usr/bin/env python
# -*- coding: utf-8 -*-

from html_to_image import html_to_image
import os

def main():
    """간단한 테스트 코드"""
    print("현재 작업 디렉토리:", os.getcwd())
    
    # 간단한 HTML 내용
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
            width=800,
            height=600
        )
        print(f"이미지가 성공적으로 생성되었습니다: {output_path}")
        
        # 파일이 존재하는지 확인
        if os.path.exists(output_path):
            print(f"파일 크기: {os.path.getsize(output_path)} 바이트")
        else:
            print("파일이 생성되지 않았습니다.")
    
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 