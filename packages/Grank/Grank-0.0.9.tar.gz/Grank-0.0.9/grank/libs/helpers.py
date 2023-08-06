import requests
import os
import configparser
import datetime
import click
import pandas as pd
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def query(query,config):
    """封装后的 GraphQL 请求"""
    if config["login"]["token"] == '':
        print("You Need Login First, Run `grank login`")
        exit()
    token = config["login"]["token"]
    headers = {"Authorization": "Bearer %s" % token}
    response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

def check_exist():
    """检测所需文件是否存在"""
    if not os.path.exists('result'):
        os.makedirs('result')
    if not os.path.exists('output'):
        os.makedirs('output')
    if os.path.isfile('grank.ini'):
        return True
    else:
        return False

def get_config():
    """读取配置文件并返回对应实例"""
    configInstance = configparser.ConfigParser()
    if not check_exist():
        configInstance = configparser.ConfigParser()
        configInstance["login"] = {}
        configInstance["login"]["token"]= ''
        configInstance["corp"] = {}
        configInstance["corp"]["keyword"]=''
        configInstance["time"] = {}
        configInstance["time"]["start_time"]='2017-01-01'
        configInstance["time"]["end_time"]= datetime.date.today().strftime('%Y-%m-%d') # 使用今天的日期
        configInstance["rank"] = {}
        configInstance["rank"]["top"] = '3' # 默认制作前三名的综合图像
        with open('grank.ini', 'w') as configfile:
            configInstance.write(configfile)
    configInstance.read('grank.ini')
    return configInstance
    pass

def set_user_token(token):
    """向配置文件写入用户 Token"""
    config = get_config();
    config["login"]["token"] = token
    with open('grank.ini','w') as configfile:
        config.write(configfile)

def set_keyword(keyword):
    """向配置文件写入关键词"""
    config = get_config();
    config["corp"]["keyword"] = keyword
    with open('grank.ini','w') as configfile:
        config.write(configfile)

def has_next_page(result,mode):
    """判断是否有下一页"""
    if mode == "pr":
        if (has_result(result,"pr")):
            if result["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]:
                return True
            else:
                return False
        else:
            return False

    if mode == "commit":
        if (has_result(result,"commit")):
            if result["data"]["repository"]["ref"]['target']["history"]["pageInfo"]["hasNextPage"]:
                return True
            else:
                return False
        else:
            return False
    if mode == "repository":
        if (has_result(result,"repository")):
            if result["data"]["organization"]["repositories"]["pageInfo"]["hasNextPage"]:
                return True
            else:
                return False
        else:
            return False

    if mode == "user_repository":
        if (has_result(result,"user_repository")):
            if result["data"]["user"]["repositories"]["pageInfo"]["hasNextPage"]:
                return True
            else:
                return False
        else:
            return False

def get_page_cursor(result,mode):
    """判断是否有对应的结果"""
    if mode == "pr":
        return result["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]

    if mode == "commit":
        return result["data"]["repository"]["ref"]['target']["history"]["pageInfo"]["endCursor"]

    if mode == "repository":
        return result["data"]["organization"]["repositories"]["pageInfo"]["endCursor"]

    if mode == "user_repository":
        return result["data"]["organization"]["repositories"]["pageInfo"]["endCursor"]

def has_result(result,mode):
    """判断是否有对应的结果"""
    if mode == "pr":
        return ("pullRequests" in result["data"]["repository"])
    elif mode == "commit":
        return ("ref" in result["data"]["repository"])
    elif mode == 'repository':
        return ('repositories' in result["data"]["organization"])
    elif mode == 'user_repository':
        return ('repositories' in result["data"]["user"])

def cover_time(time):
    """时间的简化处理"""
    if time :
        return time[0:10]
    else:
        return "未标注时间"

def add_item_to_commit_array(item,blank_array):
    """针对 commit 的数组处理"""
    blank_array.append({
            'author' : item["node"]["author"]["email"],
            'date': cover_time(item["node"]["pushedDate"]),
            "times":1
        })

def add_item_to_pr_array(item,blank_array):
    """针对 pull requests 的数组处理"""
    blank_array.append({
      "date":cover_time(item["publishedAt"]),
      "times":1
    })


def export_csv(series,name):
    """导出 Csv 文件"""
    series.to_csv("output/%s.csv" % name);

def get_avarage_instance():
    """获取平均值 DF 实例"""
    if not os.path.isfile("output/average.pkl"):
        pd.DataFrame(data={'name': [], 'score': []}).to_pickle("output/average.pkl")
    return pd.read_pickle("output/average.pkl")

def set_avarage(instance,owner,repository,score):
    """保存中间值，并更新 csv 文件"""
    instance = instance.append(pd.Series({"owner":owner,"name":repository,"score":score}),ignore_index=True)
    instance = instance.drop_duplicates(subset=["owner","name"]).sort_values(["score"],ascending=False)
    instance.to_pickle("output/average.pkl")
    instance.to_csv("result/project_rank.csv")

def series_to_pickle(df,name):
    """将数据保存到 pickle 中"""
    df.to_pickle("output/%s.pkl" % name)

def generate_line_number(start_time,end_time,top_number):
    """生成平均值的折线图"""
    df = pd.read_pickle("output/average.pkl")
    all_df = pd.DataFrame(data=[],index=pd.date_range(start=start_time,end=end_time,freq="W"))

    for index, row in df.iterrows():
        if len(all_df.columns) < top_number:
            all_df[row["name"]] = pd.read_pickle("output/%s.pkl" % row["name"])["score"]
        else:
            break

    fig = all_df.plot().get_figure()
    fig.savefig("result/line.png")
    plt.close(fig)

def is_login():
    if not 'login' in configInstance.sections():
        click.echo("You should login first")
        return False
    else:
        return True