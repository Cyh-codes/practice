import plotly.express as px
from die import Die as d

die1 = d()
die2 = d()

results = []
for i in range(1, 1000):
    result = die1.roll() * die2.roll()
    results.append(result)

frequencies = []
poss_results = []
for i in range(1, 7):
    for j in range(1, 7):
        poss_result = i * j
        if poss_result not in poss_results:
            poss_results.append(poss_result)
# sort排  很重要!!! 确保了从小到大的顺序
poss_results.sort()

for value in poss_results:
    frequency = results.count(value)
    frequencies.append(frequency)
    print(f"{value} : {frequency}")

# 核心修改：将数字转为字符串列表，打破连续数轴的限制
poss_results_str = [str(value) for value in poss_results]

title = "The Result of D6 * D6 1000 Time"
labels = {'x': 'value', 'y': 'frequency'}
fig = px.bar(x= poss_results_str, y= frequencies, title= title, labels= labels)

fig.show()

