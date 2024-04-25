import plotly.express as px
import pandas as pd


def plot_bar_chart(
    data: pd.DataFrame, x_axis: str, y_axis: str, y_axis_title: str = None
):
    bar = px.bar(
        data_frame=data,
        x=x_axis,
        y=y_axis,
    )
    bar.update_layout(yaxis_title=y_axis if y_axis_title is None else y_axis_title)

    return bar.update_xaxes(tickangle=-45)
