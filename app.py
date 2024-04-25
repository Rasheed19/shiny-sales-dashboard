from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from faicons import icon_svg
from shinywidgets import output_widget, render_widget


from utils.processor import get_sidebar_filter, get_filtered_data
from utils.plotter import plot_bar_chart


filter = get_sidebar_filter()

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_selectize(
            "cities",
            "Select cities",
            choices=filter.cities,
            selected=filter.cities[0],
            multiple=True,
        ),
        ui.input_selectize(
            "customers",
            "Select customer types",
            choices=filter.customer_types,
            selected=filter.customer_types[0],
            multiple=True,
        ),
        ui.input_selectize(
            "genders",
            "Select genders",
            choices=filter.gender,
            selected=filter.gender[0],
            multiple=True,
        ),
        ui.input_dark_mode(mode="light"),
        ui.card(
            ui.card_header("About"),
            ui.markdown(
                f"""
                This dashboad showcases how to reactively render KPIs and plots
                using shiny Python library. This project is inspired by the
                [youtube video](https://www.youtube.com/watch?v=_KaVKeP5xIA)
                which uses Taipy instead of shiny library.
                You can find the source code of this dashboard 
                and how to deploy it to various platforms
                [here](https://github.com/Rasheed19/shiny-sales-dashboard).    
            """
            ),
        ),
        width=350,
    ),
    ui.layout_column_wrap(
        ui.value_box(
            "Total Sales",
            ui.output_text("_total_sales"),
            showcase=icon_svg("magnifying-glass-dollar"),
        ),
        ui.value_box(
            "Average Sales",
            ui.output_text("_average_sales"),
            showcase=icon_svg("magnifying-glass-dollar"),
        ),
        ui.value_box(
            "Average Rating",
            ui.output_text("_average_rating"),
            showcase=icon_svg("star"),
        ),
        fill=False,
    ),
    ui.layout_column_wrap(
        *[
            ui.card(
                ui.card_header("Sales by hour"),
                output_widget("_sales_by_hour"),
            ),
            ui.card(
                ui.card_header("Sales by product line"),
                output_widget("_sales_by_product_line"),
            ),
        ]
    ),
    title="Sales dashboard",
    fillable=True,
    class_="bslib-page-dashboard",
)


def server(input: Inputs, output: Outputs, session: Session):

    @reactive.calc
    def _get_filtered_data():
        return get_filtered_data(
            cities=list(input.cities()),
            customers=list(input.customers()),
            genders=list(input.genders()),
        )

    @render.text
    def _total_sales():
        return f"$ {_get_filtered_data().df_filtered['Total'].sum():.2f}"

    @render.text
    def _average_sales():
        return f"$ {_get_filtered_data().df_filtered['Total'].mean():.2f}"

    @render.text
    def _average_rating():
        return f"{_get_filtered_data().df_filtered['Rating'].mean():.1f}"

    @render_widget
    def _sales_by_hour():
        return plot_bar_chart(
            data=_get_filtered_data().sales_by_hour,
            x_axis="Hour",
            y_axis="Total",
            y_axis_title="Sales ($)",
        )

    @render_widget
    def _sales_by_product_line():
        return plot_bar_chart(
            data=_get_filtered_data().sales_by_product_line,
            x_axis="Product line",
            y_axis="Total",
            y_axis_title="Sales ($)",
        )


app = App(app_ui, server)
