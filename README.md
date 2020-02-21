# spider_lianjia_by_metro
2020-02-21
- 爬取上海所有地铁站在链家系统中的编码
  1. 函数def lianjia_metro_station_code()
  2. 可自行更改函数内的初始url来改成其它城市
  3. 得到的上海地铁站信息存于lianjia_metro_station_code.csv，后续可掉用，也可每次调用查找函数
  4  地铁站编码用于加入url查找该地铁站周边的房源
- 主函数
  1. 可自定义地铁站名（列表）
  2. 可自定义房价下限和上限
  3. 已默认选择90-130平米，3室4室选项，如需更改可在def get_station_house()里更改url
  4. 爬取数据存于xxx_lianjia.csv
