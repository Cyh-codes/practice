import random
import plotly.graph_objects as go

class RandomWalk:
    """一个生成随机游走数据的类。"""
    def __init__(self, num_points=5000):
        self.num_points = num_points
        # 所有的游走都始于 (0, 0)
        self.x_values = [0]
        self.y_values = [0]

    def fill_walk(self):
        """计算随机游走包含的所有点。"""
        while len(self.x_values) < self.num_points:
            # 决定前进方向以及沿这个方向前进的距离
            x_direction = random.choice([1, -1])
            x_distance = random.choice([0, 1, 2, 3, 4])
            x_step = x_direction * x_distance

            y_direction = random.choice([1, -1])
            y_distance = random.choice([0, 1, 2, 3, 4])
            y_step = y_direction * y_distance

            # 拒绝原地踏步
            if x_step == 0 and y_step == 0:
                continue

            # 计算下一个点的 x 值和 y 值
            next_x = self.x_values[-1] + x_step
            # 注意修补原书可能存在的笔误：这里必须是 self.y_values[-1]
            next_y = self.y_values[-1] + y_step

            self.x_values.append(next_x)
            self.y_values.append(next_y)

# 1. 实例化随机游走并生成数据
rw = RandomWalk(num_points=5000)
rw.fill_walk()

# 2. 创建 Plotly 轨迹（Trace）
# 使用颜色渐变（color=list(range(rw.num_points))）来体现时间的先后顺序
trace_walk = go.Scatter(
    x=rw.x_values,
    y=rw.y_values,
    mode='markers',
    marker=dict(
        size=4,
        color=list(range(rw.num_points)), 
        colorscale='Viridis', 
        showscale=True,
        colorbar=dict(title="Walk Steps")
    ),
    name='Walk Path'
)

# 3. 边缘情况单独处理：高亮起点和终点
trace_start = go.Scatter(
    x=[rw.x_values[0]],
    y=[rw.y_values[0]],
    mode='markers',
    marker=dict(size=12, color='green', symbol='circle'),
    name='Start Point'
)

trace_end = go.Scatter(
    x=[rw.x_values[-1]],
    y=[rw.y_values[-1]],
    mode='markers',
    marker=dict(size=12, color='red', symbol='square'),
    name='End Point'
)

# 4. 组装数据与布局
data = [trace_walk, trace_start, trace_end]

layout = go.Layout(
    title="Random Walk Simulation (Plotly Interactive View)",
    xaxis=dict(title="X Position", showgrid=True, zeroline=True),
    yaxis=dict(title="Y Position", showgrid=True, zeroline=True),
    hovermode='closest',
    width=1000,
    height=700
)

fig = go.Figure(data=data, layout=layout)

# 5. 在浏览器中渲染交互式图表
fig.show()