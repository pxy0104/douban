# -*- coding: utf-8 -*-
# @Time    : 2023/2/24 9:53
# @File    : spider.py
# @Software: PyCharm
# @Author  : pxy

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 指定url，获取网页数据
import xlwt  # 进行excel操作
import sqlite3  # 进行SQLite数据库操作

"""
1.爬取网页
2.解析数据
3.获取数据
"""

def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    print(len(datalist))
    # print(datalist)
    # path = ".\\doubanTop250.xls"
    # saveData(datalist, path)

    # 将数据存入SQLite
    # dbpath= ".\\movie.db"
    # saveDateToDB(datalist,dbpath)
    # askURL("https://movie.douban.com/top250?start=")


# 影片详情连接的规则，制定规则把标签内指定的链接找出来
findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则（字符串的模式）
findImage = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S 忽略换行符，让换行符包含在字符中
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 参与评论人数
findReview = re.compile(r'<span>(\d*)人评价</span>')

findInq = re.compile(r'<span class="inq">(.*?)</span>')
# 找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 1.爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0, 10):  # 调用获取网页信息，10次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码
        # 2.逐一解析数据的过程
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            data = []  # 保存一部电影item全部信息
            # print(item) #测试：查看电影item全部信息
            item = str(item)
            # 影片详情链接
            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定的字符串---->获取影片的详情链接
            # print(link)
            data.append(link)

            imgSrc = re.findall(findImage, item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle, item)
            if len(titles) == 2:
                ctitle = titles[0]  # 添加中文名字
                data.append(ctitle)
                # otitle = titles[1].replace("/", "")  # 去掉无关的符号
                otitle = re.sub('/', "", titles[1])  # 替换/
                otitle = otitle.strip()
                # otitle=otitle.strip()
                data.append(otitle)  # 添加外文影名
            else:
                data.append(titles[0])
                data.append(' ')  # 外文名字留空
            rating = re.findall(findRating, item)[0]
            data.append(rating)

            reviews = re.findall(findReview, item)[0]
            data.append(reviews)

            inq = re.findall(findInq, item)
            # data.append(inq)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(" ")  # 留空

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)
            bd = re.sub(r'\xa0', "", bd)  # 替换掉所有的\xa0
            bd = re.sub('/', "", bd)  # 替换/
            bd = bd.strip()
            data.append(bd)  # 去掉前后的空格
            datalist.append(data)
            # print(data)
    return datalist


# 3.保存数据
def saveData(datalist, path):
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    worksheet = workbook.add_sheet('doubanTop250', cell_overwrite_ok=True)
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外文名", "评分", "评价人数", "概况", "相关信息")
    # print(len(col))
    for i in range(0, len(col)):
        worksheet.write(0, i, col[i])  # 写入列名
    # worksheet.write(0,0,'hello')
    for i in range(0, 250):
        # print("第 %d 条" % i+1)
        data = datalist[i]
        for j in range(0, 8):
            worksheet.write(i + 1, j, data[j])
    workbook.save(path)


def init_db(dbpath):
    sql = '''
            create table movie250
            (
            id integer primary key autoincrement,
            info_link text,
            imag_link text,
            cname varchar,
            oname varchar,
            score numeric,
            reviews numeric,
            inq text,
            bd text
            )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


def saveDateToDB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            data[index] = '"' + str(data[index]) + '"'
        sql='''insert into movie250(info_link,imag_link,cname,oname,score,reviews,inq,bd)
                values(%s)'''%",".join(data)
        # print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


def askURL(url):
    head = {
        # 模拟浏览器头部信息，像豆瓣服务器发送请求
        "User-Agent": "{Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Aoyou/RnFYKkp0ODFPS1Eqd3tFJo8eh68c-cyYBi07wZ3fMGXwmV_Uu87HlGVGiw==}"
    }  # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器，
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


if __name__ == "__main__":
    main()
    # init_db("movie.db")
    print("爬取完毕")
