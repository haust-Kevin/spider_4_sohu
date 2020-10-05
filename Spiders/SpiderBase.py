import json
import re
import time

import requests
from lxml import etree


def timestamp_2_str(time_):
    return time.strftime("%Y-%m-%d %H:%M:%S", time_)


# 保持图片正常尺寸
def _modify_img_url(img_url_origin):
    if not img_url_origin:
        return ''
    # 为不含http:的链接补充http:
    img_url = 'http://' + re.sub('(.*)//(.*)', '\\2', img_url_origin)
    # 去除对图片的裁剪
    img_url = re.sub('(.*//)(.*?/)(.*,.*?/)(.*)', '\\1\\2\\4', img_url)
    return img_url


# 保存爬取到的数据
def _save(tup):
    # param tup: tuple(url, img_url, title, source, publish_time, article)
    print((*tup[0:-2], timestamp_2_str(tup[-2])))  # 文本未打印


# 保存产生网络请求错误的url
def _save_error_url(url):
    print(url)


class SpiderBase:
    PAGE_SIZE = 20

    def __init__(self):
        pass

    # json数据源url的生成器
    def _json_url_gene(self):
        assert 0

    # 从json数据转为的dict中拿到带有每页所有文章信息的list
    def _items_of_json(self, json_data):
        return json_data

    # 发起网路请求，拿到url对应的json数据
    def _get_json(self, url):
        try:
            resp = requests.get(url)
            try:
                return json.loads(resp.text)
            except json.decoder.JSONDecodeError:
                return {'empty': True}
        except:
            _save_error_url(url)
            return None

    # 从url中提取文章正文
    def _get_article(self, url):
        try:
            html_ele = etree.HTML(requests.get(url).text)
            return html_ele.xpath('string(//*[@id="mp-editor"])')
        except:
            _save_error_url(url)
            return None

    # 拿到需要的数据
    def _get_item_info(self, item_dict):
        if 'resourceData' in item_dict:
            item_dict = item_dict['resourceData']['contentData']
            img_url = _modify_img_url(item_dict['cover']) if 'cover' in item_dict else ''
        else:
            img_url = _modify_img_url(item_dict['picUrl']) if 'picUrl' in item_dict else ''
        url = 'https://www.sohu.com/a/' + str(item_dict['id']) + '_' + str(item_dict['authorId'])
        title = item_dict['title']
        source = item_dict['authorName']
        publish_time = time.localtime(item_dict['publicTime'] / 1000)
        article = self._get_article(url)
        return url, img_url, title, source, publish_time, article

    # 爬虫启动函数
    def run(self):
        json_gen = self._json_url_gene()
        while True:
            json_url = next(json_gen)
            json_data = self._get_json(json_url)
            if not json_data:  # 网络、连接问题拿不到json数据
                continue
            if 'empty' in json_data:  # 已经拿不到数据
                break
            items = self._items_of_json(json_data)
            for item in items:
                _save(self._get_item_info(item))
            if len(items) < SpiderBase.PAGE_SIZE:
                break


if __name__ == '__main__':
    pass
