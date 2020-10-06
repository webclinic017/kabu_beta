# coding: utf-8
import re
import json
import requests
import jieba.analyse
import matplotlib as mpl
from imageio import imread
from wordcloud import WordCloud
from django.http.response import HttpResponse

# mpl.use('TkAgg')
import matplotlib.pyplot as plt

class weiboInfoFlow:

    # 基于 m.weibo.cn 抓取少量数据，无需登陆验证
    url_template = "https://m.weibo.cn/api/container/getIndex?type=wb&queryVal={}&containerid=100103type=2%26q%3D{}&page={}"


    def clean_text(self,text):
        """清除文本中的标签等信息"""
        dr = re.compile(r'(<)[^>]+>', re.S)
        dd = dr.sub('', text)
        dr = re.compile(r'#[^#]+#', re.S)
        dd = dr.sub('', dd)
        dr = re.compile(r'@[^ ]+ ', re.S)
        dd = dr.sub('', dd)
        return dd.strip()


    def fetch_data(self,query_val, page_id):
        """抓取关键词某一页的数据"""
        resp = requests.get(self.url_template.format(query_val, query_val, page_id))
        print(resp.text)
        card_group = json.loads(resp.text)['data']['cards'][0]['card_group']
        print('url：', resp.url, ' --- 条数:', len(card_group))

        mblogs = []  # 保存处理过的微博
        for card in card_group:
            mblog = card['mblog']
            blog = {'mid': mblog['id'],  # 微博id
                    'text': self.clean_text(mblog['text']),  # 文本
                    'userid': str(mblog['user']['id']),  # 用户id
                    'username': mblog['user']['screen_name'],  # 用户名
                    'reposts_count': mblog['reposts_count'],  # 转发
                    'comments_count': mblog['comments_count'],  # 评论
                    'attitudes_count': mblog['attitudes_count']  # 点赞
                    }
            mblogs.append(blog)
        return mblogs


    def remove_duplication(self,mblogs):
        """根据微博的id对微博进行去重"""
        mid_set = {mblogs[0]['mid']}
        new_blogs = []
        for blog in mblogs[1:]:
            if blog['mid'] not in mid_set:
                new_blogs.append(blog)
                mid_set.add(blog['mid'])
        return new_blogs


    def fetch_pages(self,query_val, page_num):
        """抓取关键词多页的数据"""
        mblogs = []
        for page_id in range(1 + page_num + 1):
            try:
                #obj =weiboInfoFlow()

                mblogs.extend(self.fetch_data(query_val, page_id))
            except Exception as e:
                print('fetch_pages')
                print(e)

        print("去重前：", len(mblogs))
        mblogs = self.remove_duplication(mblogs)
        print("去重后：", len(mblogs))

        # 保存到 result.json 文件中
        fp = open('result_{}.json'.format(query_val), 'w', encoding='utf-8')
        json.dump(mblogs, fp, ensure_ascii=False, indent=4)
        print("已保存至 result_{}.json".format(query_val))
        return "success"

    def getweiboinfo(request,text):
        print(text)
        obj=weiboInfoFlow()
        if obj.fetch_pages(text, 50) == "success":
            obj.gen_img_main(text)

        return HttpResponse('success')



    def keywords(mblogs):
        text = []
        for blog in mblogs:
            keyword = jieba.analyse.extract_tags(blog['text'])
            text.extend(keyword)
        return text

    def gen_img_main(self,text):
        keyword = text
        mblogs = json.loads(open('result_{}.json'.format(keyword), 'r', encoding='utf-8').read())
        print('微博总数：', len(mblogs))

        words = []
        for blog in mblogs:
            words.extend(jieba.analyse.extract_tags(blog['text']))

        print("总词数：", len(words))

        self.gen_img(words, 'edge.png')

    def gen_img(texts, img_file):
        data = ' '.join(text for text in texts)
        image_coloring = imread(img_file)
        wc = WordCloud(
            background_color='white',
            mask=image_coloring,
            font_path='/Library/Fonts/STHeiti Light.ttc'
        )
        wc.generate(data)

        # plt.figure()
        # plt.imshow(wc, interpolation="bilinear")
        # plt.axis("off")
        # plt.show()

        wc.to_file(img_file.split('.')[0] + '_wc.png')
