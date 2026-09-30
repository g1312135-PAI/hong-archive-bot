import os
import requests
import xml.etree.ElementTree as ET

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=payload)

def fetch_google_news():
    # 구글 뉴스 공식 데이터 피드 (검색어: 홍장원)
    url = "https://news.google.com/rss/search?q=%ED%99%8D%EC%9E%A5%EC%9B%90&hl=ko&gl=KR&ceid=KR:ko"
    
    response = requests.get(url)
    root = ET.fromstring(response.content)
    
    # 구글 뉴스에서 검색된 가장 최신 기사(첫 번째 item) 추출
    item = root.find('.//channel/item')
    
    if item is not None:
        title = item.find('title').text
        link = item.find('link').text
        
        message = (
            f"🎯 [아카이브 수집 알림]\n\n"
            f"📌 공식 보도 제목:\n{title}\n\n"
            f"🔗 링크:\n{link}\n\n"
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
    fetch_google_news()
