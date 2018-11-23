import pymysql
import requests
import json
from lxml import etree


def get_one_page(url, i):
    l = url[0].split('.')
    a = l[2] + '_%s' % i
    r_url = 'http:' + l[0] + '.' + l[1] + '.' + a + '.' + l[3]
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }

    response = requests.get(r_url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return None


def parse_one_page(html):
    html_etree  = etree.HTML(html)

    name_list = []
    names = html_etree.xpath('//div[@class="col-xs-12"]/a/text()')
    urls = html_etree.xpath('//div[@class="col-xs-12"]/a/@href')

    for i in  range(len(names)):
        name = {}
        name['name'] = names[i]
        name['url'] = 'http:'+urls[i]
        name_list.append(name)

    return name_list


def update_db():
    # 创建连接
    coon = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='baijiaxing')

    # 创建游标
    cursor = coon.cursor()
    urls = []
    sql = """select url from first_name"""
    cursor.execute(sql.encode('utf-8'))
    data = cursor.fetchall()
    print(data)
    coon.close()
    return data

    # for item in shops:
    #     sql = """insert into shop(name,price,image) value (%s,%s,%s)"""
    #     try:
    #         cursor.execute(sql, item['name'], item['price'], item['image'])
    #         coon.commit()
    #     except:
    #         coon.rollback()


def into_database(names_list):
    coon = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='baijiaxing')

    # 创建游标
    cursor = coon.cursor()


    # # 插入数据
    for item in names_list:
        sql = 'insert into name(name, first_name, url) values ("%s", "%s", "%s")' % (
        item['name'], item['name'][0], item['url'])
        try:
            cursor.execute(sql)
            coon.commit()
        except:
            continue

    coon.close()


def get_all_name(data):
    '''
    爬取所有姓的url
    '''
    names_list = []
    for url in data:
        print(url)
        for i in range(1, 11):
            html = get_one_page(url, i)
            print(html)
            name_list = parse_one_page(html)
            names_list.extend(name_list)
            print(url[0] + '第%s页' % i)
        into_database(names_list)



def main():
    data = update_db()
    get_all_name(data)


if __name__ == '__main__':
    main()
