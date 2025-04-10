import dash
import os
import argparse
from dash import Dash, html
import dash_bootstrap_components as dbc


_PAGE_FLAVOR = "Home"
_VERS = "phot/DR3, spec/v1.3"

debugMode = False


def setup_all(
    page_flavor=_PAGE_FLAVOR,
    vers=_VERS,
):
    external_stylesheets = [
        dbc.themes.BOOTSTRAP,
        "assets/dash_app.css",
        "assets/alt.css",
    ]

    app = Dash(
        __name__,
        use_pages=True,
        external_stylesheets=external_stylesheets,
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


if __name__ == "__main__":
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
