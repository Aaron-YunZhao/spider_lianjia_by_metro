
import pandas as pd
import re
import requests
from pyquery import PyQuery as pq
import time

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


def get_html(url_):
    headers = {
        'Cookie': 'lianjia_uuid=028a7753-4554-41c2-898e-94caff3484be; _smt_uid=5dd0b6f3.26e5d077; '
        'UM_distinctid=16e774aa5e5423-09cbdcd8085321-7711a3e-1fa400-16e774aa5e63bb; '
        '_jzqy=1.1573959412.1573959412.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6%E7%BD%91.-; '
        '_ga=GA1.2.878164124.1573959413; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216e774aa85287'
        '-0e297fb6d6d16c-7711a3e-2073600-16e774aa853552%22%2C%22%24device_id%22%3A%2216e774aa85287-0e297fb6d6d16c'
        '-7711a3e-2073600-16e774aa853552%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6'
        '%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C'
        '%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC'
        '%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22'
        '%24latest_utm_campaign%22%3A%22sousuo%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22'
        '%24latest_utm_term%22%3A%22biaoti%22%7D%7D; select_city=310000; _jzqc=1; _jzqckmp=1; _qzjc=1; '
        '_gid=GA1.2.503857469.1582108065; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1582108068; '
        'lianjia_ssid=12d68930-3a51-3fe1-2833-feb254025a0f; login_ucid=2000000001544875; '
        'lianjia_token=2.0007041d0a7db6e24d16a9343be6df9959; '
        'security_ticket=gJVpl8YcXDsQY5CBrPmMdzBXyV3QCXCZoUwJlqUYOjMqH78vTWxO5I5FD6+ssO4LGV8jNXdYA9OfQPz'
        '+EvdzvpOLklhbk2oXfHwZFIkP5sKUxhdphjACfv2IX3r8598099AHVA3pQQoSpdFfKsDilwqs0YY6bpFpEL5d9Iec8ew=; '
        'CNZZDATA1253492439=1619668075-1573957796-https%253A%252F%252Fsp0.baidu.com%252F%7C1582112792; '
        'CNZZDATA1254525948=1773823008-1573955250-https%253A%252F%252Fsp0.baidu.com%252F%7C1582110769; '
        'CNZZDATA1255633284=1474410133-1573955161-https%253A%252F%252Fsp0.baidu.com%252F%7C1582110985; '
        'CNZZDATA1255604082=190868923-1573955124-https%253A%252F%252Fsp0.baidu.com%252F%7C1582110899; '
        '_jzqa=1.3097213020792224300.1573959412.1582108063.1582114011.5; '
        '_jzqx=1.1573967211.1582114011.3.jzqsr=sh%2Elianjia%2Ecom|jzqct=/ditu.jzqsr=sh%2Elianjia%2Ecom|jzqct'
        '=/ershoufang/l3l4l5a4a5bp700ep800/; _jzqb=1.1.10.1582114011.1; _gat=1; _gat_past=1; _gat_global=1; '
        '_gat_new_global=1; _gat_dianpu_agent=1; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1582114033; '
        '_qzja=1.1942174401.1573959411644.1582108063047.1582114011028.1582114011028.1582114033092.0.0.0.85.5; '
        '_qzjb=1.1582114011028.2.0.0.0; _qzjto=13.2.0 ',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/52.0.2743.116 Safari/537.36'}
    r = requests.get(url_, headers=headers)
    # print(r.status_code)
    return r.text


def lianjia_metro_station_code():
    html_ = get_html('https://sh.lianjia.com/ditiefang/')
    # print(html_)
    doc = pq(html_)
    select = doc('div[data-role="ditiefang"] div a')
    line_df = pd.DataFrame()
    for item in select.items():
        data = [[item.text(), item.attr('href')]]
        line_df = line_df.append(data, ignore_index=True)
    line_df.columns = ['line_name', 'line_code']
    # print(line_df)

    station_df = pd.DataFrame()
    for index in line_df.index:
        line_url = 'https://sh.lianjia.com' + \
            str(line_df.loc[index, 'line_code'])
        html_ = get_html(line_url)
        pattern = re.compile(
            '<a href="/ditiefang(\S+)"   title="上海.*?站在售二手房 ">(.*?)</a>')
        data = re.findall(pattern, html_)

        data_df = pd.DataFrame(data, columns=['station_code', 'station_name'])
        data_df['line_name'] = str(line_df.loc[index, 'line_name'])
        station_df = station_df.append(data_df, ignore_index=True)
    order = ['line_name', 'station_name', 'station_code']
    station_df = station_df[order]
    print(station_df)
    station_df.to_csv('lianjia_metro_station_code.csv',
                      index=False,
                      encoding='utf_8_sig')


def parse_page(html_):
    doc = pq(html_)
    hs_url = doc('.bigImgList .item .img')  # href
    hs_title = doc('.sellListContent li div .title a')  # text
    hs_comm = doc(
        '.sellListContent li div .flood .positionInfo a[data-el="region"]')
    hs_area = hs_comm.siblings('a')
    hs_dscp = doc('.sellListContent li div .houseInfo')
    hs_fllw = doc('.sellListContent li div .followInfo')
    hs_total_p = doc('.sellListContent li div .priceInfo .totalPrice span')
    hs_unit_p = doc('.sellListContent li div .priceInfo .unitPrice span')

    hs_dic = {}
    clm = 0
    data = []
    for item in hs_url.items():
        if len(data) == 0:
            data = [item.attr('href')]
        else:
            data.append(item.attr('href'))
    hs_dic.update({clm: data})
    clm = clm + 1

    info = [
        hs_area,
        hs_comm,
        hs_dscp,
        hs_total_p,
        hs_unit_p,
        hs_fllw,
        hs_title]
    for i in info:
        data = []
        for item in i.items():
            if len(data) == 0:
                data = [item.text()]
            else:
                data.append(item.text())
        hs_dic.update({clm: data})
        clm = clm + 1
    hs_df = pd.DataFrame(hs_dic)
    if hs_df.empty:
        print('None')
        return None
    else:
        hs_df = pd.concat(
            [hs_df, hs_df[3].str.split('|', expand=True)], axis=1)
        hs_df.columns = [
            'url',
            'area',
            'community',
            'describe',
            'price',
            'unit_price',
            'input',
            'title',
            'layout',
            'size',
            'facing',
            'decorate',
            'floor',
            'year',
            'building']
        hs_df = hs_df.drop('describe', axis=1)
        print(hs_df.head())
        return hs_df


def get_station_house(station_, base_, top_):
    csv_file = "lianjia_metro_station_code.csv"
    station_df = pd.read_csv(csv_file, low_memory=False)  # 防止弹出警告
    data = None
    for item in station_:
        station_index = station_df[(
            station_df.station_name == item)].index.tolist()
        station_code = station_df.loc[station_index[0], 'station_code']
        print(item, station_code)
        for i in range(1, 3):
            url_ = 'https://sh.lianjia.com/ditiefang' + \
                str(station_code) + 'pg' + str(i) + 'l3l4a4a5bp' + str(base_) + 'ep' + str(top_) + '/'
            html_ = get_html(url_)
            page_df = parse_page(html_)
            if data is None and page_df is not None:
                data = page_df
                page_df['metro'] = item
            elif page_df is not None:
                page_df['metro'] = item
                data = data.append(page_df, ignore_index=True)
    order = ['url',
             'metro',
             'area',
             'community',
             'size',
             'layout',
             'price',
             'unit_price',
             'input',
             'floor',
             'year',
             'building',
             'facing',
             'decorate',
             'title']
    data = data[order]
    return data


if __name__ == '__main__':

    station = ['中山公园站',
               '江苏路站',
               '交通大学站',
               '上海图书馆站']
    base_price = 700  # 搜索最低价（万元）
    top_price = 900  # 搜索最高价（万元）

    df = get_station_house(station, base_price, top_price)
    # print(df.head())
    now = time.strftime("%Y-%m-%d-%H-%M", time.localtime(time.time()))
    df.to_csv(now + r'_lianjia.csv',
              index=False,
              encoding='utf_8_sig')
