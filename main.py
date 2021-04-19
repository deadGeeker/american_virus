import requests as reqs
from lxml import etree
import pandas as pd

url = "https://3g.dxy.cn/newh5/view/pneumonia"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}

data = reqs.get(url=url, headers=headers)
data.encoding = "utf-8"

# 抓取美国德特里克堡病毒在世界上的疫情现状，将目标页面的HTML数据存放到01.html
# if data.status_code == reqs.codes.ok:
#     with open("01.html", "w", encoding="utf-8") as f:
#         f.write(str(data.text))

# 分离数据中的国家、确诊人数、治愈人数、死亡人数
html_data = etree.HTML(data.text, etree.HTMLParser())
html_data = html_data.xpath('//*[@id="getListByCountryTypeService2true"]/text()')

# 去头去尾 截取中间的数据
# 头：print(len("try { window.getListByCountryTypeService2true = [']"))
# 尾：print(len("catch(e){}']"))
html1_data = html_data[0][49:-12]

# print(html1_data)
# 将截取后的数据存储到02.txt中
# with open("02.txt", "w", encoding="utf-8") as f:
#     f.write(str(html1_data))

# eval不支持null，true，false等，没法正确转换为None，True，False
# print(type(html1_data))
html1_data = html1_data.replace('true', 'True')
html1_data = html1_data.replace('false', 'False')
html1_data = eval(html1_data)
# print(type(html1_data[0]))

country = []
confirmed = []
lived = []
dead = []

for i in html1_data:
    country.append(i['provinceName'])
    confirmed.append(i['confirmedCount'])
    lived.append(i['curedCount'])
    dead.append(i['deadCount'])

data_world = pd.DataFrame()
data_world['国家名称'] = country
data_world['确诊人数'] = confirmed
data_world['治愈人数'] = lived
data_world['死亡人数'] = dead

# dataframe数据格式文件转.xlsx文件
data_world.to_excel("01.xlsx")
# print(data_world)

