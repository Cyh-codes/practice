import matplotlib.pyplot as plt

x_values = range(2,100)
y_values = [x ** 3 for x in x_values]

plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.scatter(x_values, y_values, c=y_values, cmap = plt.cm.Blues, s=20)

ax.set_title('lifang', fontsize=15)
ax.set_xlabel('Numbers', fontsize=12)
ax.set_ylabel('Numbers ** 3', fontsize=12)

ax.axis([0, 101, 1, 100_000_0])
ax.ticklabel_format(style = 'plain')

plt.show()