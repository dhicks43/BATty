import dash_html_components as html

navbar = html.Nav(
        className="navbar navbar-expand-lg navbar-dark bg-dark fixed-top",
        children=[
            html.Div(
                className="container",
                children=[
                    html.A("BATty", className="navbar-brand", href="#"),
                    html.Div(className="navbar-nav ml-auto", id="navbarResponsive",
                            children=[
                            html.Ul(className="navbar-nav ml-auto",
                                    children=[
                                        html.Li(className="nav-item active",
                                                children=[
                                                    html.A(
                                                        "About",
                                                        className="nav-link",
                                                        href="http://www.darrylhicks.us",
                                                       )

                                                ]
                                                )
                                 ]
                                )
                                ]
                             )
                ]
             )]
    )