# 종이 추첨권 생성기

이메일 목록과 조직명만으로 번호가 부여된 추첨권을 생성하는 프로그램입니다.

## 기능

- CSV 파일의 이메일 목록을 읽어서 각각 고유 번호 부여
- 사용자 지정 조직명/행사명으로 추첨권 생성
- 번호가 부여된 추첨권을 HTML 형식으로 생성
- 추첨권은 보관용/추첨용으로 분리되어 있으며 절취선 포함
- A4 용지 크기에 맞춰 자동 정렬
- 추첨권 번호는 오름차순으로 정렬
- 한 번의 명령으로 전체 과정 완료

## 사용 방법

1. 이메일 목록 준비
   - CSV 파일에 이메일 목록을 저장합니다 (예: `emails.csv`)
   - CSV 파일은 한 줄에 하나의 이메일 주소가 있어야 합니다.

2. 추첨권 생성

   ```bash
   python3 lottery_generator.py [이메일파일] "[조직명]"
   ```

   **사용 예시:**

   ```bash
   # 기본 사용
   python3 lottery_generator.py emails.csv "2024 우리 회사"
   
   # 출력 파일명 지정
   python3 lottery_generator.py emails.csv "게임 동호회" -o my_tickets.html
   
   # 도움말 보기
   python3 lottery_generator.py --help
   ```

3. 추첨권 인쇄
   - 생성된 HTML 파일을 웹 브라우저에서 엽니다.
   - 프린터 설정에서 다음 사항을 확인합니다:
     - 용지 크기: A4
     - 크기 조정: "실제 크기" 또는 "크기 조정 없음" 선택
     - 여백: 기본값 사용

## 파일 구조

- `lottery_generator.py`: 추첨권 생성 스크립트
- `emails.csv`: 원본 이메일 목록 (입력 파일)
- `tickets.html`: 생성된 추첨권 HTML 파일 (출력 파일)

## 추첨권 형식

- 크기: 320px x 90px
- 구성: 보관용(좌) + 절취선 + 추첨용(우)
- 포함 정보:
  - 행사명/조직명: 사용자 지정 (예: "2024 게임동호회")
  - 추첨권 번호
  - 발행 날짜 (자동 생성)
  - 용도 구분(보관용/추첨용)

## 요구사항

- Python 3.x
- 웹 브라우저
- A4 용지 출력이 가능한 프린터

## 빠른 시작

```bash
# 1. 이메일 목록 파일 준비 (emails.csv)
echo "test1@example.com" > emails.csv
echo "test2@example.com" >> emails.csv
echo "test3@example.com" >> emails.csv

# 2. 추첨권 생성
python3 lottery_generator.py emails.csv "우리 행사"

# 3. tickets.html 파일을 브라우저에서 열어 인쇄
```
