#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

def create_bar_chart():
    """막대 그래프 생성"""
    months = ['1월', '2월', '3월', '4월', '5월', '6월']
    sales = [65, 59, 80, 81, 56, 55]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=sales,
        text=sales,
        textposition='auto',
        marker_color=['rgba(255, 99, 132, 0.8)', 'rgba(54, 162, 235, 0.8)', 
                      'rgba(255, 206, 86, 0.8)', 'rgba(75, 192, 192, 0.8)',
                      'rgba(153, 102, 255, 0.8)', 'rgba(255, 159, 64, 0.8)']
    ))
    
    fig.update_layout(
        title='월별 판매량',
        xaxis_title='월',
        yaxis_title='판매량',
        template='plotly_white'
    )
    
    return fig

def create_line_chart():
    """선 그래프 생성"""
    months = ['1월', '2월', '3월', '4월', '5월', '6월']
    visitors = [12, 19, 3, 5, 2, 3]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=visitors,
        mode='lines+markers',
        marker=dict(size=10, color='rgba(75, 192, 192, 0.8)'),
        line=dict(width=3, color='rgba(75, 192, 192, 0.8)')
    ))
    
    fig.update_layout(
        title='월별 방문자 수',
        xaxis_title='월',
        yaxis_title='방문자 수',
        template='plotly_white'
    )
    
    return fig

def create_pie_chart():
    """파이 차트 생성"""
    labels = ['빨강', '파랑', '노랑', '초록', '보라', '주황']
    values = [12, 19, 3, 5, 2, 3]
    
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        textinfo='label+percent',
        insidetextorientation='radial',
        marker=dict(
            colors=['rgba(255, 99, 132, 0.8)', 'rgba(54, 162, 235, 0.8)', 
                    'rgba(255, 206, 86, 0.8)', 'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)', 'rgba(255, 159, 64, 0.8)']
        )
    ))
    
    fig.update_layout(
        title='선호 색상',
        template='plotly_white'
    )
    
    return fig

def create_combined_chart():
    """복합 그래프 생성"""
    months = ['1월', '2월', '3월', '4월', '5월', '6월']
    sales = [300, 450, 380, 420, 550, 600]
    profit = [100, 200, 150, 180, 250, 300]
    satisfaction = [80, 85, 75, 90, 95, 92]
    
    # 서브플롯 생성
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # 매출액 (막대)
    fig.add_trace(
        go.Bar(
            x=months,
            y=sales,
            name="매출액 (만원)",
            marker_color='rgba(54, 162, 235, 0.8)'
        ),
        secondary_y=False,
    )
    
    # 순이익 (막대)
    fig.add_trace(
        go.Bar(
            x=months,
            y=profit,
            name="순이익 (만원)",
            marker_color='rgba(255, 99, 132, 0.8)'
        ),
        secondary_y=False,
    )
    
    # 고객 만족도 (선)
    fig.add_trace(
        go.Scatter(
            x=months,
            y=satisfaction,
            name="고객 만족도 (%)",
            mode='lines+markers',
            line=dict(color='rgba(75, 192, 192, 0.8)', width=3),
            marker=dict(size=8)
        ),
        secondary_y=True,
    )
    
    # 레이아웃 업데이트
    fig.update_layout(
        title_text="월별 매출 및 고객 만족도",
        template='plotly_white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # x축 레이블
    fig.update_xaxes(title_text="월")
    
    # y축 레이블
    fig.update_yaxes(title_text="금액 (만원)", secondary_y=False)
    fig.update_yaxes(title_text="만족도 (%)", secondary_y=True, range=[0, 100])
    
    return fig

def create_heatmap():
    """히트맵 생성"""
    # 데이터 생성
    np.random.seed(42)
    data = np.random.randint(0, 100, size=(10, 10))
    
    # 히트맵 생성
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=[f'항목 {i+1}' for i in range(10)],
        y=[f'카테고리 {i+1}' for i in range(10)],
        colorscale='Viridis',
        showscale=True
    ))
    
    fig.update_layout(
        title='히트맵 예시',
        template='plotly_white'
    )
    
    return fig

def create_html_with_plotly_graphs(output_file='plotly_graphs.html'):
    """Plotly 그래프를 포함한 HTML 파일 생성"""
    # 그래프 생성
    bar_fig = create_bar_chart()
    line_fig = create_line_chart()
    pie_fig = create_pie_chart()
    combined_fig = create_combined_chart()
    heatmap_fig = create_heatmap()
    
    # 각 그래프를 HTML로 변환
    bar_html = bar_fig.to_html(full_html=False, include_plotlyjs=False)
    line_html = line_fig.to_html(full_html=False, include_plotlyjs=False)
    pie_html = pie_fig.to_html(full_html=False, include_plotlyjs=False)
    combined_html = combined_fig.to_html(full_html=False, include_plotlyjs=False)
    heatmap_html = heatmap_fig.to_html(full_html=False, include_plotlyjs=False)
    
    # HTML 템플릿
    html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plotly 그래프 테스트</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Malgun Gothic', '맑은 고딕', Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        
        header {{
            background: linear-gradient(135deg, #0078d7, #83c3f7);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        h1 {{
            margin: 0;
            font-size: 2.2em;
        }}
        
        .content {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            margin-bottom: 30px;
        }}
        
        .graph-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin: 20px 0;
            justify-content: center;
        }}
        
        .chart-wrapper {{
            flex: 1 1 45%;
            min-height: 400px;
            border: 1px solid #eaeaea;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            background-color: white;
            margin-bottom: 20px;
        }}
        
        .chart-large {{
            flex: 1 1 100%;
        }}
        
        footer {{
            text-align: center;
            margin-top: 30px;
            color: #666;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Plotly 인터랙티브 그래프 테스트</h1>
        <p>HTML 내 인터랙티브 그래프를 이미지로 변환하기</p>
    </header>
    
    <div class="content">
        <h2>기본 그래프</h2>
        <p>Plotly를 사용한 기본적인 그래프 유형을 보여줍니다. 이러한 그래프는 인터랙티브하며 마우스 오버 시 추가 정보를 표시합니다.</p>
        
        <div class="graph-container">
            <div class="chart-wrapper">
                {bar_html}
            </div>
            
            <div class="chart-wrapper">
                {line_html}
            </div>
            
            <div class="chart-wrapper">
                {pie_html}
            </div>
            
            <div class="chart-wrapper">
                {heatmap_html}
            </div>
        </div>
    </div>
    
    <div class="content">
        <h2>복합 그래프</h2>
        <p>다중 축과 여러 그래프 유형을 결합한 복합 그래프 예시입니다.</p>
        
        <div class="chart-wrapper chart-large">
            {combined_html}
        </div>
    </div>
    
    <footer>
        <p>© 2023 Plotly 그래프 이미지 변환 테스트</p>
    </footer>
</body>
</html>
"""
    
    # HTML 파일 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"Plotly 그래프가 포함된 HTML 파일이 '{output_file}'에 저장되었습니다.")
    return output_file

if __name__ == "__main__":
    # HTML 파일 생성
    html_file = create_html_with_plotly_graphs('plotly_graphs.html')
    
    print("\n이 HTML 파일을 이미지로 변환하기 위해서는 다음 명령어를 실행하세요:")
    print(f"python simple_html_to_image.py {html_file} plotly_output.png")
    
    # 프로그램 내에서 직접 이미지 변환 실행
    try:
        from simple_html_to_image import html_to_image
        
        print("\n자동으로 이미지 변환을 시작합니다...")
        output_path = html_to_image(
            html_file=html_file,
            output_image=r"C:\Users\MZC01-younghun\Downloads\plotly_output.png",
            wait_time=5
        )
        print(f"이미지가 성공적으로 생성되었습니다: {output_path}")
    except ImportError:
        print("\nsimple_html_to_image 모듈을 찾을 수 없습니다.")
        print("수동으로 변환 명령을 실행해주세요.")
    except Exception as e:
        print(f"\n이미지 변환 중 오류 발생: {e}")
        print("수동으로 변환 명령을 실행해주세요.")


