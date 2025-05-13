#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import asyncio
from playwright.async_api import async_playwright
import tempfile


async def html_to_image_async(html_content=None, html_file=None, output_image="output.png", width=1024, height=768):
    """HTML을 이미지로 변환합니다 (비동기 함수).
    
    Args:
        html_content (str, optional): HTML 문자열 내용. 기본값은 None.
        html_file (str, optional): HTML 파일 경로. 기본값은 None.
        output_image (str, optional): 출력 이미지 파일 경로. 기본값은 "output.png".
        width (int, optional): 브라우저 뷰포트 너비. 기본값은 1024.
        height (int, optional): 브라우저 뷰포트 높이. 기본값은 768.
    
    Returns:
        str: 생성된 이미지 파일 경로
    """
    if not html_content and not html_file:
        raise ValueError("HTML 내용이나 파일 경로를 제공해야 합니다.")
    
    async with async_playwright() as p:
        # 브라우저 시작
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": width, "height": height})
        page = await context.new_page()
        
        # HTML 로드
        if html_content:
            # 임시 HTML 파일 생성
            with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_html_path = f.name
            
            # 파일 URL로 로드
            await page.goto(f'file://{temp_html_path}')
            os.unlink(temp_html_path)  # 임시 파일 삭제
        else:
            # 파일 또는 URL 로드
            if html_file.startswith('http'):
                await page.goto(html_file)
            else:
                await page.goto(f'file://{os.path.abspath(html_file)}')
        
        # 페이지 내용이 모두 로드될 때까지 대기
        await page.wait_for_load_state('networkidle')
        
        # 스크린샷 저장
        await page.screenshot(path=output_image, full_page=True)
        
        # 브라우저 닫기
        await browser.close()
        
        print(f"이미지가 '{output_image}'에 저장되었습니다.")
        return output_image


def html_to_image(html_content=None, html_file=None, output_image="output.png", width=1024, height=768):
    """HTML을 이미지로 변환합니다 (동기 래퍼).
    
    Args:
        html_content (str, optional): HTML 문자열 내용. 기본값은 None.
        html_file (str, optional): HTML 파일 경로. 기본값은 None.
        output_image (str, optional): 출력 이미지 파일 경로. 기본값은 "output.png".
        width (int, optional): 브라우저 뷰포트 너비. 기본값은 1024.
        height (int, optional): 브라우저 뷰포트 높이. 기본값은 768.
    
    Returns:
        str: 생성된 이미지 파일 경로
    """
    return asyncio.run(html_to_image_async(
        html_content=html_content,
        html_file=html_file,
        output_image=output_image,
        width=width,
        height=height
    ))


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='HTML을 이미지로 변환합니다.')
    
    # 입력 그룹 생성 (HTML 내용 또는 파일 중 하나만 선택)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--html-content', type=str, help='변환할 HTML 문자열')
    input_group.add_argument('--html-file', type=str, help='변환할 HTML 파일 경로')
    
    # 출력 관련 인수
    parser.add_argument('--output', type=str, default='output.png', help='출력 이미지 파일 경로 (기본값: output.png)')
    parser.add_argument('--width', type=int, default=1024, help='브라우저 뷰포트 너비 (기본값: 1024)')
    parser.add_argument('--height', type=int, default=768, help='브라우저 뷰포트 높이 (기본값: 768)')
    
    args = parser.parse_args()
    
    # HTML을 이미지로 변환
    try:
        output_path = html_to_image(
            html_content=args.html_content,
            html_file=args.html_file,
            output_image=args.output,
            width=args.width,
            height=args.height
        )
        print(f"변환 완료! 이미지가 생성되었습니다: {output_path}")
    except Exception as e:
        print(f"오류 발생: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 