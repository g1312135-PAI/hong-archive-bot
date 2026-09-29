import os
import requests
from bs4 import BeautifulSoup

# 보안 금고에 넣어둔 텔레그램 정보 불러오기
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=payload)

def fetch_news():
    # 네이버 뉴스 '홍장원 국정원' 검색 결과 (최신순)
    search_url = "https://search.naver.com/search.naver?where=news&query=%ED%99%8D%EC%9E%A5%EC%9B%90+%EA%B5%AD%EC%A0%95%EC%9B%90&sort=1"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 첫 번째 기사 추출
    articles = soup.find_all('a', class_='news_tit')
    if articles:
        top_article = articles[0]
        title = top_article.get('title')
        link = top_article.get('href')
        
        message = f"🚨 최신 뉴스 알림 🚨\n\n제목: {title}\n링크: {link}\n\n*내용을 확인하고 업로드할까요?*"
        send_telegram_message(message)
    else:
        print("새로운 뉴스가 없습니다.")

if __name__ == "__main__":
    fetch_news()
