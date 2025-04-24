import dash

from dash import html

from .utils_funcs import navbar_home, make_headerbar
from .file_io import _VERS_PHOT, _VERS_SPEC

_VERS = f"phot/{_VERS_PHOT}, spec/{_VERS_SPEC}"


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
