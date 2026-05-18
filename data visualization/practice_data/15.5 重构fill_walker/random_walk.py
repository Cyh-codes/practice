from random import choice

class RandomWalk:
    # 生成一个随机游走数据的类

    def __init__(self, num_points = 5000):
        # 初始化随机游走的属性
        self.num_points = num_points

        # 所有随机游走都始于(0, 0)
        self.x_values = [0]
        self.y_values = [0]

    def get_step(self):
        # 重构fill_walk 缩小规模
        n_direction = choice([-1, 1])
        n_distance = choice([0, 1, 4, 9])
        return n_direction * n_distance
    
    def fill_walk(self):
        while len(self.x_values) < self.num_points:
            x_step = self.get_step()
            y_step =self.get_step()
            if x_step == 0 and y_step == 0:
                continue
            x = self.x_values[-1] + x_step
            y = self.y_values[-1] + y_step
            self.x_values.append(x)
            self.y_values.append(y)

