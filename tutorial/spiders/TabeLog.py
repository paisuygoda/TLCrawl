# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TabeLogItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
domain = "aomori"
"""prefectures = [
        'hokkaido',
        'aomori',
        'iwate',
        'miyagi',
        'akita',
        'yamagata',
        'fukushima',
        'ibaraki',
        'tochigi',
        'gunma',
        'saitama',
        'chiba',
        'tokyo',
        'kanagawa',
        'niigata',
        'toyama',
        'ishikawa',
        'fukui',
        'yamanashi',
        'nagano',
        'gifu',
        'shizuoka',
        'aichi',
        'mie',
        'shiga',
        'kyoto',
        'osaka',
        'hyogo',
        'nara',
        'wakayama',
        'tottori',
        'shimane',
        'okayama',
        'hiroshima',
        'yamaguchi',
        'tokushima',
        'kagawa',
        'ehime',
        'kochi',
        'fukuoka',
        'saga',
        'nagasaki',
        'kumamoto',
        'oita',
        'miyazaki',
        'kagoshima',
        'okinawa',
    ]
    """
categories = [
        'RC010101'
    ]
"""    ,   # 懐石・会席料理
        'RC010103',   # 割烹・小料理
        'RC010105',   # 精進料理
        'RC010104',   # 京料理
        'RC0102',     # 寿司・魚介類
        'RC0103',     # 天ぷら・揚げ物
        'RC0104',     # そば・うどん・麺類
        'RC0105',     # うなぎ・どじょう
        'RC0106',     # 焼鳥・串焼・鳥料理
        'RC0107',     # すき焼き・しゃぶしゃぶ
        'RC0108',     # おでん
        'RC0109',     # お好み焼き・たこ焼き
        'RC0110',     # 郷土料理
        'RC0111',     # 丼もの
        'RC0199',     # 和食（その他）
        'RC0201',     # ステーキ・ハンバーグ
        'RC0203',     # 鉄板焼き
        'RC0202',     # パスタ・ピザ
        'RC020401',  # ハンバーガー
        'RC0209',     # 洋食・欧風料理
        'RC021101',     # フレンチ
        'RC021201',    # イタリアン
        'RC0219',     # 西洋各国料理
        'RC0301',     # 中華料理
        'RC0302',     # 餃子・肉まん
        'RC0303',     # 中華粥
        'RC0304',     # 中華麺
        'RC040101',      # 韓国料理
        'RC0402',     # 東南アジア料理
        'RC0403',     # 南アジア料理
        'RC0404',     # 西アジア料理
        'RC0411',     # 中南米料理
        'RC0412',     # アフリカ料理
        'RC0499',     # アジア・エスニック（その他）
        'RC1201',     # カレーライス
        'RC1202',     # 欧風カレー
        'RC1203',     # インドカレー
        'RC1204',     # タイカレー
        'RC1205',     # スープカレー
        'RC1299',     # カレー（その他）
        'RC1301',     # 焼肉・ホルモン
        'RC1302',     # ジンギスカン
        'RC2102',     # ダイニングバー
        'RC2199',     # 居酒屋・ダイニングバー（その他）
        'RC9901',     # 定食・食堂
        'RC9902',     # 創作料理・無国籍料理
        'RC9903',     # 自然食・薬膳
        'RC9904',     # 弁当・おにぎり
        'RC9999',     # レストラン（その他）
        'MC01',      # ラーメン
        'MC11',       # つけ麺
        'SC0101',     # パン
        'SC0201',     # 洋菓子
        'SC0202',     # 和菓子・甘味処
        'SC0203',     # 中華菓子
        'SC0299',     # スイーツ（その他）
    ]
    """


class TabeLogSpider(scrapy.Spider):
    name = 'TabeLogSpider'
    # allowed_domains = ['https://tabelog.com/']

    start_urls = ['http://tabelog.com/'+domain+'/rstLst/'+category+'/' for category in categories]

    custom_settings = {
        "DOWNLOAD_DELAY": 2.0,
    }

    def parse(self, response):
        link_list = response.xpath('//li//a[@class="list-rst__rst-name-target cpy-rst-name"]/@href').extract()
        name_list = response.xpath('//li//a[@class="list-rst__rst-name-target cpy-rst-name"]/text()').extract()
        globe = 1

        for link, name in zip(link_list, name_list):
            # 店ごとに必要な情報をTabelogcrawlItemに格納。
            item = TabeLogItem()
            item['name'] = name
            item['link'] = link
            item['num'] = globe
            globe += 1

            if globe == 2:
                request = scrapy.http.Request(
                    url=link, callback=self.parse_child)
                request.meta["item"] = item
                yield request
            """
            # 店の緯度経度を取得する為、
            # 詳細ページもクローリングしてTabelogcrawlItemに格納。
            request = scrapy.http.Request(
                url=link, callback=self.parse_child)
            request.meta["item"] = item
            yield request
            """

        # 次ページ。
        next_page = response.xpath('//link[@rel="next"]/@href')
        if next_page:
            href = next_page.get('href')
            #return scrapy.http.Request(url=href, callback=self.parse)

    def parse_child(self, response):
        # 店の緯度経度を抽出する。
        g = response.xpath('//div//img[@class="js-map-lazyload"]/@data-original').extract()
        g = g[0].split("center=")
        gg = g[1].split("&markers")
        longitude, latitude = gg[0].split(",")
        item = response.meta["item"]
        print("focus: " + item['name'])
        item['longitude'] = longitude
        item['latitude'] = latitude
        item['image_urls'] = []
        photo_url = response.xpath('//li[@id="rdnavi-photo"]//a[@class="mainnavi"]/@href').extract()

        # さらに写真取得へ
        request = scrapy.http.Request(
            url=photo_url[0], callback=self.parse_photo)
        request.meta["item"] = item
        return request

    def parse_photo(self, response):
        item = response.meta["item"]
        item['image_urls'] += response.xpath('//div[@class="thum-photobox__img"]/a/@href').extract()
        next_page = response.xpath('//link[@rel="next"]/@href')
        if next_page:
            href = next_page.get('href')
            request = scrapy.http.Request(url=href, callback=self.parse_photo)
            request.meta["item"] = item
            return request
        else:
            return item

    pass
