import dash

from dash import html

from .utils_funcs import navbar_home, theme_toggler


# _PAGE_FLAVOR = "Home"
_VERS = "phot/DR3, spec/v1.3"


def setup_all(
    # page_flavor=_PAGE_FLAVOR,
    vers=_VERS,
):
    dash.register_page(
        __name__,
        path="/",
        # title=f"UNCOVER Data Viewer: {page_flavor} {vers}",
        title=f"UNCOVER Data Viewer: {vers}",
    )
    # print(theme_toggler)

    layout = html.Div(
        [
            html.Div(
                [
                    html.H2(
                        children=[
                            html.A(
                                "UNCOVER",
                                href="https://jwst-uncover.github.io",
                            ),
                            f" Data Viewer: {vers}",
                        ],
                        style={"margin-bottom": "0"},
                    ),
                    html.H1("TEST2"),
                    theme_toggler(),
                ],
            ),
            navbar_home(),
        ],
    )

    return layout


layout = setup_all()
