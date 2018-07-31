##Version 0.2.30

import backend_sqlite as be
import dash
import datetime
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import app_layouts as al
import comm_names as cm
import numpy as np

app = dash.Dash()
app.title = "BATty"
server = app.server


app.css.append_css({"external_url": 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'})
app.css.append_css({"external_url": "https://cdn.rawgit.com/dhicks43/blog-code/master/portfolio-item.css"})

app.scripts.append_script({"external_url": "https://code.jquery.com/jquery-3.3.1.min.js"})
app.scripts.append_script({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.1/js/bootstrap.bundle.min.js"})

app.layout = html.Div([

    al.navbar,

    html.Div(
        className="container",
        children=[
            html.Div(className="container",
                     children=[
                         html.Div(
                            className="row my-4",
                            children=[
                                dcc.Markdown("# **Brand**", id="active-car-brand"),
                                dcc.Markdown("&ensp;"),
                                dcc.Markdown("# Model", id="active-car-model")]
                         ),

                         dcc.Dropdown(
                            id='car-brands',
                            options=[
                                {'label': _[0].replace("_", "-"), 'value': _[0]} for _ in be.view_brands()
                                ],
                            value="Brand"
                            ),

                        html.Br(),

                        dcc.Dropdown(id='brand-models', options=[], value="Model"),

                        html.Hr(),

                        html.Div(id="final_graph_div",
                                children=[
                                html.Div(id="final_graph"),
                                html.Br(),
                                html.Div(id="final_graph-info", className="row justify-content-between")
                                ]
                        ),
                        html.Br()

                    ])
        ]
    )

])


@app.callback(dash.dependencies.Output('active-car-brand', 'children'),
              [dash.dependencies.Input('car-brands', 'value')])
def populate_active_brand(active_brand):
    active_brand_string = "Please pick a model!"

    if active_brand:
        active_brand_string = "# **" + active_brand.replace("_", "-") + "**"

    return active_brand_string


@app.callback(dash.dependencies.Output('active-car-model', 'children'),
              [dash.dependencies.Input('car-brands', 'value'),
              dash.dependencies.Input('brand-models', 'value')])
def populate_active_model(active_brand, active_model):
    active_model_string = ""

    if active_model and be.active_model_in_brand(active_brand, active_model):
        active_model_string = "# " + active_model

    return active_model_string


@app.callback(dash.dependencies.Output('brand-models', 'options'),
              [dash.dependencies.Input('car-brands', 'value')],)
def populate_models(chosen_brand):
    final_list = []
    for car_model in be.view_models(chosen_brand):
        if cm.common_names[car_model[0]]:
            final_list.append(
                {'label': car_model[0] + " " + cm.common_names[car_model[0]], 'value': car_model[0]}
            )

        else:
            final_list.append(
                {'label': car_model[0], 'value': car_model[0]}
            )

    return final_list


@app.callback(dash.dependencies.Output('final_graph', 'children'),
              [dash.dependencies.Input('car-brands', 'value'),
               dash.dependencies.Input('brand-models', 'value')]
              )
def populate_chart(brand, model):
    if brand and model and be.active_model_in_brand(brand, model):
        chart_data = be.model_brand_return(model, brand)
        chart_data.sort(key=lambda r: datetime.datetime.fromtimestamp(r[0]))

        x_values = [datetime.datetime.fromtimestamp(ts[0]) for ts in chart_data]
        y_values = [price[1] for price in chart_data]
        annotation_values = ["""<a href="https://bringatrailer.com/listing/{}"> </a>""".format(title_sub[2]) for title_sub in chart_data]

        plot_annotations = []

        for val in range(len(x_values)):
            plot_annotations.append(dict(
                x=x_values[val],
                y=y_values[val],
                text=annotation_values[val],
                showarrow=False,
                xanchor='center',
                yanchor='middle'

            ))

        final_graph = dcc.Graph(
            figure=go.Figure(
                layout=
                    go.Layout(
                        title=str(brand).replace("_", "-") + " " + str(model),
                        xaxis=dict(title="Time frame"),
                        yaxis=dict(title="Price"),
                        annotations=plot_annotations
                    ),

                data=[
                    go.Scatter(
                        x=x_values,
                        y=y_values,
                        mode='lines+markers'
                    )],

                ),
            id="Bepis"
        )

        return final_graph

    return


@app.callback(dash.dependencies.Output('final_graph-info', 'children'),
              [dash.dependencies.Input('car-brands', 'value'),
              dash.dependencies.Input('brand-models', 'value'),
               dash.dependencies.Input('final_graph', 'children')])
def populate_info(final_brand, final_model, final_graph_data):
    if final_graph_data:
        final_date = datetime.datetime.timestamp(
            datetime.datetime.strptime(final_graph_data['props']['figure']['data'][0]['x'][-1], '%Y-%m-%d %X')
        )
        final_car_data = be.grab_last_car_data(final_brand, final_model, final_date)
        title, titlesub, url = final_car_data[0]

        total_y_values = final_graph_data['props']['figure']['data'][0]['y']

        # Last Car Sold
        last_car_sold_div = html.Div(id="last-car-sold", className="col-sm ml-auto", children=[])
        last_car_sold = dcc.Markdown("##### Last Car Sold:")
        last_car_sold.children += "\n " + title.lstrip("No Reserve: ") + " " + titlesub.lower()
        last_car_sold_div.children.append(last_car_sold)
        last_car_sold_div.children.append(html.A("Link", href=('https://bringatrailer.com/listing/' + url), target='_blank'))

        # Market Statistics
        market_statistics_div = html.Div(id="market-statistics", className="col-sm float-right", children=[])

        market_statistics = dcc.Markdown(
            "###### Mean:           ${:,.2f}\n"
            "###### Median:         ${:,.2f}\n"
            "###### Std. Deviation: ${:,.2f}\n".format(
                np.mean(total_y_values),
                np.median(total_y_values),
                np.std(total_y_values))
            , className="float-sm-right")

        market_statistics_div.children.append(market_statistics)

        return last_car_sold_div, html.Br(), market_statistics_div

    return


if __name__ == '__main__':
    app.run_server()
