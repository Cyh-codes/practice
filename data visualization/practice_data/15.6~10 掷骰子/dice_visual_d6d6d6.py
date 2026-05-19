import plotly.express as px

from die import Die

# 创建3个 D6
die_1 = Die()
die_2 = Die()
die_3 = Die()

results = []
for roll_num in range(1, 1000):
    result = die_1.roll() + die_2.roll() + die_3.roll()
    results.append(result)

frequencies = []
max_result = die_1.num_sides + die_2.num_sides + die_3.num_sides
poss_results = range(3, max_result)
for value in poss_results:
    frequency = results.count(value)
    frequencies.append(frequency)
    print(f"{value} : {frequency}")

title = 'Result of Rolling Three D6 1000 Times'
labels = {'x': 'value', 'y': 'frequency'}
fig = px.bar(x=poss_results, y=frequencies, title=title, labels=labels)

fig.show()