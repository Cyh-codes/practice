import plotly.express as px

from die import Die

# 创建两个 D8
die_1 = Die(8)
die_2 = Die(8)

# 投掷骰子并将其记录到列表里
results = []
for roll_num in range(1, 1000):
    result = die_1.roll() + die_2.roll()
    results.append(result)

# 分析结果,算骰子和 出现频率
frequencies = []
poss_results = []
max_result = die_1.num_sides + die_2.num_sides
for value in range(2, max_result+1):
    frequency = results.count(value)
    poss_results.append(value)
    frequencies.append(frequency)
    print(f"{value}:{frequency}")

# 对结果可视化
title = "The Result of Two D8 1000 Times"
labels = {'x': 'value', 'y': 'frequency'}
fig = px.bar(x = poss_results, y = frequencies, title = title, labels = labels)

# 进一步定制图形,加横线
fig.update_layout(xaxis_dtick = 1)

fig.show()



