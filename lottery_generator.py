#!/usr/bin/env python3
"""
추첨권 생성기 - 통합 버전
이메일 목록과 조직명만으로 추첨권을 생성합니다.
"""

import csv
import random
import sys
import argparse
from datetime import datetime
from pathlib import Path


def read_emails(email_file):
    """이메일 파일에서 이메일 목록을 읽어옵니다."""
    emails = []
    try:
        with open(email_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0]:  # 빈 줄 제외
                    emails.append(row[0].strip())
    except FileNotFoundError:
        print(f"오류: '{email_file}' 파일을 찾을 수 없습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"오류: 이메일 파일을 읽는 중 문제가 발생했습니다: {e}")
        sys.exit(1)
    
    if not emails:
        print("오류: 이메일 목록이 비어있습니다.")
        sys.exit(1)
    
    return emails


def assign_numbers(emails):
    """이메일 목록에 랜덤 번호를 할당합니다."""
    numbers = list(range(1, len(emails) + 1))
    random.shuffle(numbers)
    return list(zip(emails, numbers))


def create_ticket_html_content(number, current_date, organization_name):
    """개별 추첨권 HTML 콘텐츠를 생성합니다."""
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


def generate_tickets_html(email_number_pairs, organization_name, output_file):
    """추첨권 HTML을 생성합니다."""
    # 번호로 정렬
    numbers = sorted([pair[1] for pair in email_number_pairs])
    
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
    
    def create_page_content(numbers_list):
        content = '<div class="ticket-container">'
        for col in range(COLUMNS_PER_PAGE):
            for row in range(TICKETS_PER_COLUMN):
                index = col * TICKETS_PER_COLUMN + row
                if index >= len(numbers_list):
                    break
                
                number = numbers_list[index]
                if number is None:
                    content += '<div class="ticket empty-ticket">' + create_ticket_html_content(0, current_date, organization_name) + '</div>'
                else:
                    content += create_ticket_html_content(number, current_date, organization_name)
        
        content += '</div>'
        return content
    
    # 페이지별로 티켓 생성
    for page_numbers in pages_numbers:
        html_content += create_page_content(page_numbers)
    
    html_content += '''
    </div>
    </body>
    </html>
    '''
    
    # HTML 파일 저장
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"✅ 추첨권이 생성되었습니다: {output_file}")
        print(f"📊 총 {total_numbers}개의 추첨권이 {total_pages}페이지에 걸쳐 생성되었습니다.")
    except Exception as e:
        print(f"오류: HTML 파일을 저장하는 중 문제가 발생했습니다: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='이메일 목록으로부터 추첨권을 생성합니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
사용 예시:
  python3 lottery_generator.py emails.csv "2024 우리 회사"
  python3 lottery_generator.py emails.csv "게임 동호회" -o my_tickets.html
        '''
    )
    
    parser.add_argument('email_file', help='이메일 목록이 담긴 CSV 파일')
    parser.add_argument('organization_name', help='조직명 또는 행사명')
    parser.add_argument('-o', '--output', default='tickets.html', 
                       help='출력 HTML 파일명 (기본값: tickets.html)')
    
    args = parser.parse_args()
    
    # 입력 파일 확인
    if not Path(args.email_file).exists():
        print(f"오류: '{args.email_file}' 파일이 존재하지 않습니다.")
        sys.exit(1)
    
    print(f"📧 이메일 파일: {args.email_file}")
    print(f"🏢 조직명: {args.organization_name}")
    print(f"📄 출력 파일: {args.output}")
    print("-" * 50)
    
    # 이메일 읽기
    print("📖 이메일 목록을 읽는 중...")
    emails = read_emails(args.email_file)
    print(f"✅ {len(emails)}개의 이메일을 발견했습니다.")
    
    # 번호 할당
    print("🎲 번호를 할당하는 중...")
    email_number_pairs = assign_numbers(emails)
    print("✅ 번호 할당 완료")
    
    # 추첨권 생성
    print("🎫 추첨권을 생성하는 중...")
    generate_tickets_html(email_number_pairs, args.organization_name, args.output)
    
    print("\n🎉 모든 작업이 완료되었습니다!")
    print(f"💡 '{args.output}' 파일을 웹브라우저에서 열어 인쇄하세요.")


if __name__ == "__main__":
    main()