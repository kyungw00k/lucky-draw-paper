import csv
from datetime import datetime
import sys

def create_ticket_html(input_file, output_file):
    # 번호 목록과 조직명 읽기 및 정렬
    numbers = []
    organization_name = ""
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            numbers.append(int(row['Number']))
            if not organization_name:  # 첫 번째 행에서 조직명 가져오기
                organization_name = row.get('Organization', '2024 카카오 게임동호회')
    numbers.sort()  # 오름차순 정렬
    
    # 한 페이지에 들어갈 수 있는 티켓 수 계산
    TICKETS_PER_COLUMN = 5  # 세로로 들어갈 수 있는 티켓 수
    COLUMNS_PER_PAGE = 2    # 가로로 들어갈 수 있는 열 수
    TICKETS_PER_PAGE = TICKETS_PER_COLUMN * COLUMNS_PER_PAGE
    
    # 전체 페이지 수 계산
    total_numbers = len(numbers)
    total_pages = (total_numbers + TICKETS_PER_PAGE - 1) // TICKETS_PER_PAGE
    
    # 페이지별 번호 재배치
    pages_numbers = [[] for _ in range(total_pages)]
    for i, number in enumerate(numbers):
        page_index = i % total_pages
        pages_numbers[page_index].append(number)
    
    # 각 페이지의 번호 목록을 필요한 크기로 맞추기
    max_numbers_per_page = TICKETS_PER_PAGE
    for page_numbers in pages_numbers:
        while len(page_numbers) < max_numbers_per_page:
            page_numbers.append(None)
    
    # HTML 시작
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {
                size: A4;
                margin: 2cm;
            }
            body {
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                width: 100%;
            }
            .page {
                box-sizing: border-box;
                padding: 0;
                width: 100%;
            }
            .ticket-container {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 0.8cm;
                justify-content: center;
                align-items: start;
                page-break-inside: avoid;
                margin: 0 auto;
                max-width: 17cm;
            }
            .ticket {
                display: flex;
                border: 2px solid #ccc;
                position: relative;
                height: 90px;
                width: 320px;
                margin: 0 auto;
            }
            .ticket-half {
                flex: 1;
                padding: 12px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
            .ticket-half.keep {
                background-color: #f0f7ff;
            }
            .ticket-half.draw {
                background-color: #fff0f0;
            }
            .ticket-title {
                font-size: 11px;
                font-weight: bold;
                color: #333;
                margin-bottom: 3px;
            }
            .ticket-type {
                font-size: 13px;
                color: #666;
                margin-bottom: 4px;
            }
            .ticket-number {
                font-size: 22px;
                font-weight: bold;
                color: #333;
            }
            .ticket-date {
                font-size: 11px;
                color: #666;
                margin-top: 4px;
            }
            .dotted-line {
                border-right: 2px dashed #999;
                height: 100%;
                position: absolute;
                left: 50%;
                transform: translateX(-50%);
            }
            @media print {
                html, body {
                    width: 210mm;
                    height: 297mm;
                    margin: 0;
                    padding: 0;
                }
                .ticket-container {
                    margin-bottom: 0.8cm;
                }
                .ticket {
                    page-break-inside: avoid;
                }
            }
            .empty-ticket {
                visibility: hidden;
            }
        </style>
    </head>
    <body>
    <div class="page">
    '''
    
    # 현재 날짜
    current_date = datetime.now().strftime("%Y.%m.%d")
    
    def create_page_content(numbers_list, org_name):
        content = '<div class="ticket-container">'
        for col in range(COLUMNS_PER_PAGE):
            for row in range(TICKETS_PER_COLUMN):
                index = col * TICKETS_PER_COLUMN + row
                if index >= len(numbers_list):
                    break
                
                number = numbers_list[index]
                if number is None:
                    content += '<div class="ticket empty-ticket">' + create_ticket_html_content(0, current_date, org_name) + '</div>'
                else:
                    content += create_ticket_html_content(number, current_date, org_name)
        
        content += '</div>'
        return content
    
    # 홀이지별로 티켓 생성
    for page_numbers in pages_numbers:
        html_content += create_page_content(page_numbers, organization_name)
    
    html_content += '''
    </div>
    </body>
    </html>
    '''
    
    # HTML 파일 저장
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    print(f"완료! {output_file} 파일이 생성되었습니다.")
    print(f"총 {total_numbers}개의 추첨권이 {total_pages}페이지에 걸쳐 생성되었습니다.")

def create_ticket_html_content(number, current_date, organization_name):
    return f'''
    <div class="ticket">
        <div class="ticket-half keep">
            <div class="ticket-title">{organization_name}</div>
            <div class="ticket-type">보관용</div>
            <div class="ticket-number">No. {number}</div>
            <div class="ticket-date">{current_date}</div>
        </div>
        <div class="dotted-line"></div>
        <div class="ticket-half draw">
            <div class="ticket-title">{organization_name}</div>
            <div class="ticket-type">추첨용</div>
            <div class="ticket-number">No. {number}</div>
            <div class="ticket-date">{current_date}</div>
        </div>
    </div>
    '''

# 실행
create_ticket_html('emails_with_numbers.csv', 'tickets.html') 