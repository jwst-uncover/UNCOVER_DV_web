import dash
import os
import argparse
from dash import Dash, html, Input, Output, clientside_callback

import dash_bootstrap_components as dbc


_PAGE_FLAVOR = "Home"
_VERS = "phot/DR3, spec/v1.3"

debugMode = False


def setup_all(
    page_flavor=_PAGE_FLAVOR,
    vers=_VERS,
):
    external_stylesheets = [
        dbc.icons.FONT_AWESOME,
        dbc.icons.BOOTSTRAP,
        dbc.themes.BOOTSTRAP,
        "assets/dash_app.css",
        "assets/alt.css",
    ]
    external_scripts = ["assets/docs-theme-change.js"]

    app = Dash(
        __name__,
        use_pages=True,
        external_stylesheets=external_stylesheets,
        external_scripts=external_scripts,
        suppress_callback_exceptions=True,
    )
    app.title = f"UNCOVER Data Viewer: {page_flavor} {vers}"

    app.layout = html.Div(
        [
            dash.page_container,
        ]
    )

    return app


def create_parser():
    # handle command line arguments with argparse
    parser = argparse.ArgumentParser(description="URL+Port options for DV")

    _DV_HOST = os.environ.get("DV_URL", "0.0.0.0")
    _DV_PORT = os.environ.get("DV_PORT", 8020)

    parser.add_argument(
        "--host",
        default=_DV_HOST,
        metavar="Host URL",
        type=str,
        help="Specify the host URL",
    )

    parser.add_argument(
        "--port",
        default=_DV_PORT,
        type=int,
        help="Specify this host port",
    )

    return parser


clientside_callback(
    """
    function(n_clicks){
        window.show_active_theme();
        return n_clicks;
    }
    """,
    Output(
        component_id="bd-theme-on-load-output", component_property="children"
    ),
    Input(component_id="bd-theme-on-load", component_property="n_clicks"),
)


clientside_callback(
    """
    function(){
        const triggered_id = dash_clientside.callback_context.triggered_id;
        const theme = triggered_id.split("select-")[1];
        window.toggle_theme(theme);
    }
    """,
    Input("select-light", "n_clicks"),
    Input("select-dark", "n_clicks"),
    Input("select-auto", "n_clicks"),
)


def main():
    # read in command line arguments
    parser = create_parser()
    args = parser.parse_args()

    import datetime

    print(f"dash_app : {datetime.datetime.now()} * pre setup", flush=True)

    app = setup_all()

    print(f"dash_app : {datetime.datetime.now()} * post setup", flush=True)

    from pages.file_io import preload_all_data

    preload_all_data()

    print(
        f"dash_app : {datetime.datetime.now()} * post preload data", flush=True
    )

    if debugMode:
        print(f"{debugMode=}", flush=True)
        app.run(
            debug=True,
            host=args.host,
            port=args.port,
        )

    else:
        from waitress import serve

        serve(app.server, host=args.host, port=args.port, url_scheme="https")

        print(
            f"dash_app : {datetime.datetime.now()} * post server", flush=True
        )


if __name__ == "__main__":
    main()
