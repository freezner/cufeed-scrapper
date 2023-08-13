import hashlib

import feedparser
import ssl
from django.http import JsonResponse
from cufeedScrapServer.models import Feeds


# 헬스 체크
def health_check(request):
    return JsonResponse(status=200, data={'status': 'true', 'message': 'OK'})


# 뉴스 수집
def collect_news(request, site, keyword):
    hash_salt = "gudwls2smsthrmawhgdmgka!"
    vendor = "google"  # 지금은 구글 밖에 없음.

    try:
        if site == 'google':
            url = 'https://news.google.com/rss/search?q=' + keyword + '+when:1d&hl=ko&gl=KR&ceid=KR:ko'
        else:
            raise ValueError

        ssl._create_default_https_context = ssl._create_unverified_context
        rss = feedparser.parse(url)

        for item in rss.entries:
            title = item.title
            link = item.link
            link_hash = hashlib.md5((title + link + hash_salt).encode("utf-8")).hexdigest()

            # 뉴스 제목이 같은 건 스킵한다.
            valid_count = Feeds.objects.filter(title=title).count()

            # 같은 link_hash가 존재해도 등록하지 않고 스킵한다.
            valid_count = valid_count + Feeds.objects.filter(link_hash=link_hash).count()

            if valid_count > 0:
                print("Already content:", title)
            else:
                # TODO: keyword는 id로 변경해야함.
                record = Feeds(title=title, link=link, link_hash=link_hash, vendor=vendor, keyword=keyword)
                record.save()

            print("title:", title, ", link:", link)

        return JsonResponse(status=200, data={'status': 'true', 'message': 'OK'})
    except ValueError:
        return JsonResponse(status=400, data={'status': 'false', 'message': 'Bad request'})
