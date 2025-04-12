import dash

from dash import html

from .utils_funcs import navbar_home, make_headerbar

_VERS = "phot/DR3, spec/v1.3"


def setup_all(
    vers=_VERS,
):
    dash.register_page(
        __name__,
        path="/",
        title=f"UNCOVER Data Viewer: {vers}",
    )

    headerbar = make_headerbar(
        h2_entry=[
            html.A(
                "UNCOVER",
                href="https://jwst-uncover.github.io",
            ),
            f" Data Viewer: {vers}",
        ]
    )

    layout = html.Div(
        [
            html.Div(
                headerbar,
            ),
            navbar_home(),
        ],
    )

    return layout


layout = setup_all()
