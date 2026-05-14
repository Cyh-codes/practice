import matplotlib.pyplot as plt

x_values = [1, 3, 5, 7, 9]
y_values = [x ** 3 for x in x_values]

plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.scatter(x_values, y_values, s=200)

ax.set_title('lifang', fontsize=15)
ax.set_xlabel('Numbers', fontsize=12)
ax.set_ylabel('Numbers ** 3', fontsize=12)

ax.axis([0, 10, 1, 800])
ax.ticklabel_format(style = 'plain')

plt.show()