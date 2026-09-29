import os
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=payload)

def fetch_history_news():
    # 검색어: '홍장원 내란' (2024년 12월 사태 및 이후 공식 행보 집중 검색)
    search_url = "https://search.naver.com/search.naver?where=news&query=%ED%99%8D%EC%9E%A5%EC%9B%90+%EB%82%B4%EB%9E%80&sort=1"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = soup.find_all('a', class_='news_tit')
    
    if articles:
        top_article = articles[0]
        title = top_article.get('title')
        link = top_article.get('href')
        
        # 질문자님의 마음이 담긴 템플릿 구조화
        message = (
            f"🎯 [아카이브 수집 알림]\n\n"
            f"📌 공식 보도 제목:\n{title}\n\n"
            f"🔗 권위자/공식 링크:\n{link}\n\n"
            f"--- [게시판 업로드용 코멘트 초안] ---\n"
            f"2024년 겨울, 국가와 국민을 위해 내린 소신 있는 결단을 기억합니다. "
            f"역사가 평가할 그날의 진실이 더 널리 알려지기를 바라며 변함없이 응원합니다.\n"
            f"----------------------------------\n\n"
            f"✅ 이 내용 그대로 우리 게시판에 발행할까요?"
        )
        send_telegram_message(message)
    else:
        print("관련 뉴스가 없습니다.")

if __name__ == "__main__":
    fetch_history_news()
