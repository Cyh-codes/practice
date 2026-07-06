from operator import itemgetter
import plotly.express as px
import requests

# 执行 API  调用查看响应
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
r = requests.get(url)
print(f"Status Code: {r.status_code}")

# 处理每篇文章的信息
submission_ids = r.json()
titles, hn_links, comments = [], [], []
for submission_id in submission_ids[:30]:
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    # print(f"Status Code: {r.status_code}")
    # 跳过status code死的
    if r.status_code != 200:
        continue

    response_dict = r.json()

    # 核心修改：使用 try-except 结构忽略没有评论数（descendants）或标题的招聘帖子
    try:
        title = response_dict['title']
        # 某些帖子可能没有 descendants 键（即 0 条评论或招聘贴），捕获它
        comments_count = response_dict.get('descendants', 0)
    except KeyError:
        # 忽略特殊的招聘帖子，继续处理下一个
        continue
    hn_link = f"https://news.ycombinator.com/item?id={submission_id}"
    title_link = f"<a href='{hn_link}'>{title}</a>"
    titles.append(title_link)
    comment = response_dict['descendants']
    comments.append(comment)
# 直接让 comments 参与排序，并让 titles 保持对应的顺序（条形图从高到低）
# 使用 zip 将标题和评论数绑定在一起，按评论数降序排序后拆开
sorted_data = sorted(zip(comments, titles), key=itemgetter(0), reverse=True)
comments, titles = [list(x) for x in zip(*sorted_data)]

# 可视化
title = 'Hacker-News'
labels = {'x': 'Title', 'y': 'Comments'}
fig = px.bar(x=titles, y=comments, title=title, labels=labels)
fig.update_traces(marker_color='SteelBlue', marker_opacity=0.6)
fig.write_html('python_hn_submissions_visual.html')
print("生成完成:python_hn_submissions_visual.html")
