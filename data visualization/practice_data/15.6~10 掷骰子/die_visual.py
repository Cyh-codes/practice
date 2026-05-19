import plotly.express as px

from die import Die

# 创建两个 D6
die_1 = Die()
die_2 = Die()

# 掷几次骰子并将结果存储在一个列表中
# 改为列表推导式!!!
results = [die_1.roll() + die_2.roll() for i in range(1, 1000)]

# 分析结果
# 同样改为列表推导式
max_result = die_1.num_sides + die_2.num_sides
poss_results = range(1, max_result+1)
frequencies = [results.count(value) for value in poss_results]

# 对结果进行可视化
title ='Result of Rolling Two D6 1000 Times'
labels = {'x': 'Result', 'y': 'Frequency of Result'}
fig = px.bar(x=poss_results, y=frequencies, title=title, labels =labels)

# 进一步定制图形
fig.update_layout(xaxis_dtick=1)

fig.show()

