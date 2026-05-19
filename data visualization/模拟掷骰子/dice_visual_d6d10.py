import plotly.express as px
from die import Die

# 创建一个 D6 和 一个 D10
die_1 = Die()
die_2 = Die(10)

# 投掷骰子多次,并将结果存储到列表里
results = []
for roll_num in range(50_000):
    result = die_1.roll() + die_2.roll()
    results.append(result)

# 分析结果
frequencies = []
max_result = die_1.num_sides + die_2.num_sides
poss_results = range(1, max_result+1)
for value in poss_results:
    frequency = results.count(value)
    frequencies.append(frequency)

# 可视化结果
title = "Die 6 AND Die 10"
labels = {'x': 'Result', 'y': 'Frequency of result'}
fig = px.bar(x= poss_results, y= frequencies, title = title, labels = labels)

# 进一步定制图形
fig.update_layout(xaxis_dtick=1)

fig.show()

# 保存图形
fig.write_html('dice_visual_d6d10.html')
