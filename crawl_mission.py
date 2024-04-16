import requests
import os
import re

# 固定图片类别列表
categories = ['叶子卡通', '香蕉卡通', '西瓜卡通', '黄芒果卡通', '草莓卡通', '柠檬卡通', '青苹果卡通', '西红柿卡通',
              '红苹果卡通', '李子卡通']
total_num_of_pics = 50

# 共享请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}

# 初始化计数器及存储路径
downloaded_count = 0
duplicates_count = 0
failures_count = 0
base_path = os.getcwd()
data_path = os.path.join(base_path, 'data')

# 确保data目录存在
if not os.path.exists(data_path):
    os.makedirs(data_path)

# 遍历图片类别
for category in categories:
    category_dir = os.path.join(data_path, category)
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)

    # 下载每个类别的图片
    for pn in range(0, total_num_of_pics, 30):  # 每页30张图片，根据需要下载的总数量调整页数
        url = f'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={category}&pn={pn}'
        res = requests.get(url, headers=headers)
        htlm_1 = res.content.decode()

        # 匹配图片URL
        a = re.findall('"objURL":"(.*?)",', htlm_1)
        for b in a:
            try:
                b_1 = re.findall('https:(.*?)&', b)[0]
                img_url = ''.join(b_1)

                # 防止重复下载
                if img_url not in b_1:
                    img_res = requests.get(img_url)
                    filename = f'{category}_{downloaded_count}.jpg'
                    filepath = os.path.join(category_dir, filename)

                    with open(filepath, 'ab') as f:
                        print(f'---------正在下载第{downloaded_count + 1}张图片----------')
                        f.write(img_res.content)

                    downloaded_count += 1
                    if downloaded_count >= total_num_of_pics:
                        break  # 达到指定下载数量后退出循环

                else:
                    duplicates_count += 1
                    continue

            except Exception as e:
                failures_count += 1
                print(f'---------第{downloaded_count + 1}张图片无法下载----------')
                continue

    if downloaded_count >= total_num_of_pics:
        break  # 所有类别加起来达到指定下载数量后退出类别循环

print('下载完成,总共下载{}张,成功下载:{}张,重复下载:{}张,下载失败:{}张'.format(
    downloaded_count + duplicates_count + failures_count, downloaded_count, duplicates_count, failures_count))

# 注意：上述代码仍无法精确筛选出卡通风格的图片，因此实际下载的图片可能不全是卡通风格。