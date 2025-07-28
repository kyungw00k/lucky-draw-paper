import csv
import random
import sys

def assign_random_numbers(input_file, output_file, organization_name):
    # 이메일 목록 읽기
    emails = []
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            emails.append(row[0])
    
    # 이메일 개수만큼의 랜덤 번호 생성
    numbers = list(range(1, len(emails) + 1))
    random.shuffle(numbers)
    
    # 이메일과 번호 매칭하여 새로운 CSV 파일 작성
    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Email', 'Number', 'Organization'])  # 헤더에 조직명 추가
        for email, number in zip(emails, numbers):
            writer.writerow([email, number, organization_name])
    
    print(f"완료! {output_file} 파일이 생성되었습니다.")

# 실행
if __name__ == "__main__":
    if len(sys.argv) > 1:
        organization_name = sys.argv[1]
    else:
        organization_name = input("조직명을 입력하세요: ")
    
    assign_random_numbers('emails.csv', 'emails_with_numbers.csv', organization_name) 