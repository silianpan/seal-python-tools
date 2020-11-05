import json
import re
import pymysql
from fake_useragent import UserAgent
from pyspider.libs.base_handler import *
pattern_article = re.compile(u'^https://med.sina.com/article_detail_.+.html$')
urls = ['https://med.sina.com/column/zonghe/','https://med.sina.com/feature_322.html','https://med.sina.com/feature_284.html','https://med.sina.com/feature_1341.html']

class Handler(BaseHandler):
    crawl_config = {}
    def __init__(self):
        self.conn = pymysql.connect(host='172.16.95.1', user='root', password='Asdf@123', port=3306, db='db-biotown-gdss')
        self.cursor = self.conn.cursor()
    def __del__(self):
        self.conn.close()
    def get_taskid(self, task):
        return md5string(task['url']) + json.dumps(task['fetch'].get('data', ''))
    @every(minutes=24 * 60)
    def on_start(self):
        for url in urls:
            self.crawl(url, validate_cert=False, method='GET', callback=self.index_page, user_agent=UserAgent().random)

    @config(age=5 * 24 * 60 * 60)
    def index_page(self, response):
        next_page = response.doc('.show > .clickmore_f')
        if next_page is None:
            next_page = response.doc('.show > .clickmore_f')
        if next_page is not None:
            sign = next_page.attr('sign')
            if sign is not None:
                next_url_prefix1 = 'https://med.sina.com/article_list_'
                next_url_prefix2 = 'https://med.sina.com/feature_list_'
                next_url = ''
                signs = sign.strip().split('_')
                if len(signs) == 4:
                    next_sign = int(signs[2]) + 1
                    next_url = next_url_prefix1 + signs[0] + '_' + signs[1] + '_' + str(next_sign) + '_' + signs[3] + '.html'
                else:
                    next_sign = int(signs[1]) + 1
                    next_url = next_url_prefix2 + signs[0] + '_' + str(next_sign) + '_' + signs[2] + '.html'
                self.crawl(next_url, validate_cert=False, method='GET', callback=self.index_page,
                           user_agent=UserAgent().random)
        self.item_page(response)
    def item_page(self, response):
        ua = UserAgent()
        for each in response.doc('a[href^="http"]').items():
            if re.match(pattern_article, each.attr.href):
                self.crawl(each.attr.href, validate_cert=False, callback=self.detail_page, user_agent=ua.random)
    @config(priority=2)
    def detail_page(self, response):
        title = response.doc('.news > h1.news-title').text().strip()
        source = response.doc('.news > .wz-tbbox > .wz-zuthorname > em').text().strip()
        pub_date = response.doc('.news > .wz-tbbox > .wz-fbtime').text().strip()
        content = response.doc('.news > .textbox').html().strip()
        ret = {
            'url': response.url,
            'title': title,
            'content': content,
            'pub_date': pub_date,
            'source': source
        }
        self.save_to_mysql(ret)
        return ret
    def save_to_mysql(self, ret):
        insert_sql = """
        INSERT INTO spider_med_sina(url, title, content, pub_date, source) values(%s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(insert_sql, (
                ret.get('url', ''), ret.get('title', ''), ret.get('content', ''),
                ret.get('pub_date', ''), ret.get('source', '')))
            self.conn.commit()
        except pymysql.err.IntegrityError:
            print('Repeat Key')
