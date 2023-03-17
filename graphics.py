import plotly.graph_objects as go
import plotly.figure_factory as ff


x = [[], [], [], []]
y = [[], [], [], []]
x_a = [[], [], [], []]
y_a = [[], [], [], []]
x_s = [[], [], [], [], [], []]
y_s = [[], [], [], [], [], []]
av_x_t = list()
av_y_t = list()
av_x_h = list()
av_y_h = list()
av_x_grh = list()
av_y_grh = list()


def plot_graph_temperatyre(x_time, values):
    global x, y
    c = 0
    for elem in values:
        y[c].append(elem)
        x[c].append(x_time)
        c += 1
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x[0], y=y[0], name="Датчик 1"))
    fig.add_trace(go.Scatter(x=x[1], y=y[1], name="Датчик 2"))
    fig.add_trace(go.Scatter(x=x[2], y=y[2], name="Датчик 3"))
    fig.add_trace(go.Scatter(x=x[3], y=y[3], name="Датчик 4"))
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5, xanchor="center"),
                      title="Теплица",
                      xaxis_title="Время t, мин",
                      yaxis_title="Температура t, C",
                      margin=dict(l=0, r=0, t=30, b=0))


    fig.write_image("static/graphs/all_temp.png")


def plot_graph_airhyd(x_time, values):
    global x_a, y_a
    c = 0
    for elem in values:
        y_a[c].append(elem)
        x_a[c].append(x_time)
        c += 1
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_a[0], y=y_a[0], name="Датчик 1"))
    fig.add_trace(go.Scatter(x=x_a[1], y=y_a[1], name="Датчик 2"))
    fig.add_trace(go.Scatter(x=x_a[2], y=y_a[2], name="Датчик 3"))
    fig.add_trace(go.Scatter(x=x_a[3], y=y_a[3], name="Датчик 4"))
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5, xanchor="center"),
                      title="Теплица",
                      xaxis_title="Время t, мин",
                      yaxis_title="Влажность воздуха p, %",
                      margin=dict(l=0, r=0, t=30, b=0))


    fig.write_image("static/graphs/all_airhyd.png")

def plot_graph_soilhyd(x_time, values):
    global x_s, y_s
    c = 0
    for elem in values:
        y_s[c].append(elem)
        x_s[c].append(x_time)
        c += 1
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_s[0], y=y_s[0], name="Датчик 1"))
    fig.add_trace(go.Scatter(x=x_s[1], y=y_s[1], name="Датчик 2"))
    fig.add_trace(go.Scatter(x=x_s[2], y=y_s[2], name="Датчик 3"))
    fig.add_trace(go.Scatter(x=x_s[3], y=y_s[3], name="Датчик 4"))
    fig.add_trace(go.Scatter(x=x_s[4], y=y_s[4], name="Датчик 5"))
    fig.add_trace(go.Scatter(x=x_s[5], y=y_s[5], name="Датчик 6"))
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5, xanchor="center"),
                      title="Теплица",
                      xaxis_title="Время t, мин",
                      yaxis_title="Влажность почвы p, %",
                      margin=dict(l=0, r=0, t=30, b=0))


    fig.write_image("static/graphs/all_soilhyd.png")


def plot_graph_average_temp(x_time, values):
    global av_x_t, av_y_t
    av_x_t.append(x_time)
    av_y_t.append(values)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=av_x_t, y=av_y_t, name="Измерение средней температуры"))
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5, xanchor="center"),
                      title="Теплица",
                      xaxis_title="Время t, мин",
                      yaxis_title="Температура t, C",
                      margin=dict(l=0, r=0, t=30, b=0))


    fig.write_image("static/graphs/averagetemperature.png")


def plot_graph_average_hyd(x_time, values):
    global av_x_h, av_y_h
    av_x_h.append(x_time)
    av_y_h.append(values)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=av_x_h, y=av_y_h, name="Измерение средней влажности воздуха"))
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5, xanchor="center"),
                      title="Теплица",
                      xaxis_title="Время t, мин",
                      yaxis_title="Влажность воздуха p, %",
                      margin=dict(l=0, r=0, t=30, b=0))


    fig.write_image("static/graphs/averagehydration.png")


def plot_graph_average_soilhyd(x_time, values):
    global av_x_grh, av_y_grh
    av_x_grh.append(x_time)
    av_y_grh.append(values)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=av_x_grh, y=av_y_grh, name="Измерение средней влажности воздуха"))
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5, xanchor="center"),
                      title="Теплица",
                      xaxis_title="Время t, мин",
                      yaxis_title="Влажность почвы p, %",
                      margin=dict(l=0, r=0, t=30, b=0))


    fig.write_image("static/graphs/averagesoilhydration.png")

def draw_table(args):
    data_matrix = [['Время', 'Средняя влажность воздуха', 'Средняя влажность почвы', 'Средняя температура почвы'],
               ['1 минута', args[0][0], args[0][1], args[0][2]],
               ['5 минут', args[1][0], args[1][1], args[1][2]],
               ['10 минут', args[2][0], args[2][1], args[2][2]],
               ['30 минут', args[3][0], args[3][1], args[3][2]],
               ['1 час', args[4][0], args[4][1], args[4][2]],
               ['12 часов', args[5][0], args[5][1], args[5][2]],
               ['Все время', args[6][0], args[6][1], args[6][2]]]

    fig = ff.create_table(data_matrix)
    fig.update_layout(width=1000)
    fig.write_image("static/graphs/table.png")



def clear():
    global x, y, x_a, y_a, x_s, y_s, av_x_t, av_y_t, av_x_h, av_y_h, av_x_grh, av_y_grh
    if len(av_x_t) >= 20:
        av_x_t = av_x_t[(len(av_x_t) - 20):]
        av_y_t = av_y_t[(len(av_y_t) - 20):]
        av_x_h = av_x_h[(len(av_x_h) - 20):]
        av_y_h = av_y_h[(len(av_y_h) - 20):]
        av_x_grh = av_x_grh[(len(av_x_grh) - 20):]
        av_y_grh = av_y_grh[(len(av_y_grh) - 20):]
        x = [f[(len(f) - 20):] for f in x]
        y = [f[(len(f) - 20):] for f in y]
        x_a = [f[(len(f) - 20):] for f in x_a]
        y_a = [f[(len(f) - 20):] for f in y_a]
        x_s = [f[(len(f) - 20):] for f in x_s]
        y_s = [f[(len(f) - 20):] for f in y_s]
