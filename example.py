#!/usr/bin/env python
# -*- coding: utf-8 -*-

from html_to_image import html_to_image

# HTML 문자열을 이미지로 변환하는 예제
def example_from_string():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>간단한 HTML 예제</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f0f0f0; }
            h1 { color: #0066cc; text-align: center; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; background-color: white; border-radius: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>안녕하세요!</h1>
            <p>이것은 HTML 문자열에서 생성된 이미지입니다.</p>
            <p>이 예제는 <strong>HTML 문자열</strong>을 이미지로 변환하는 방법을 보여줍니다.</p>
            <p>한글 텍스트 테스트: 가나다라마바사</p>
        </div>
    </body>
    </html>
    """
    
    output_path = html_to_image(
        html_content=html_content,
        output_image="from_string.png",
        width=800,
        height=600
    )
    print(f"HTML 문자열에서 이미지 생성 완료: {output_path}")

# HTML 파일을 이미지로 변환하는 예제
def example_from_file():
    output_path = html_to_image(
        html_file="test.html",
        output_image="from_file.png",
        width=1024,
        height=768
    )
    print(f"HTML 파일에서 이미지 생성 완료: {output_path}")

if __name__ == "__main__":
    print("HTML 문자열에서 이미지 생성 중...")
    example_from_string()
    
    print("\nHTML 파일에서 이미지 생성 중...")
    example_from_file()
    
    print("\n두 가지 예제가 모두 실행되었습니다. 생성된 이미지 파일을 확인해보세요.") 