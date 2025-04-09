import pathlib

import dash
import dash_ag_grid as dag
from dash import html


from .utils_funcs import navbar_tables

from .file_io import global_store, make_column_defs

_PAGE_FLAVOR = "Phot Sample"
_VERS = "DR3"

_DICT_TABLE_ENTRIES = {
    "id": {
        "from": "phot",
        "header": "id",
        "cellRenderer": "OverviewPhotLink",
        "format": "d",
    },
    "z_phot_50": {
        "from": "sps",
        "format": "0.3f",
    },
    "magF444W": {
        "format": "0.2f",
    },
    "lmstar_50": {
        "from": "sps",
        "format": "0.2f",
    },
    "sfr100_50": {
        "from": "sps",
        "format": "0.2e",
    },
    "ssfr100_50": {
        "from": "sps",
        "format": "0.2e",
    },
    "mu_50": {
        "from": "sps",
        "format": "0.2f",
    },
    "use_phot": {
        "from": "phot",
    },
    "ra": {
        "from": "phot",
        "format": "0.8f",
    },
    "dec": {
        "from": "phot",
        "format": "0.8f",
    },
    "id_spec": {
        "from": "sample_spec",
        "cellRenderer": "OverviewSpecLink",
        "catkey": "specid",
        "format": "d",
    },
    "z_spec": {
        "from": "spec",
        "format": "0.3f",
    },
}

path = pathlib.Path(__file__).parent.parent.resolve()
_FNAME_DF = f"{path}/assets/data/df_sample_phot_index.fits"


def setup_all(
    page_flavor=_PAGE_FLAVOR,
    vers=_VERS,
    fname_DF=_FNAME_DF,
    dict_table_entries=_DICT_TABLE_ENTRIES,
):
    columnDefs = make_column_defs(dict_table_entries)
    df = global_store(fname_DF)

    dash.register_page(
        __name__,
        path="/phot/",
        title=f"UNCOVER Data Viewer: {page_flavor} {vers}",
    )

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
                            f" Data Viewer: {page_flavor} {vers}",
                        ],
                        style={"margin-bottom": "0"},
                    ),
                ],
            ),
            navbar_tables(),
            dag.AgGrid(
                id="sample",
                rowData=df.to_dict("records"),
                columnDefs=columnDefs,
                defaultColDef={
                    "resizable": True,
                    "sortable": True,
                    "filter": True,
                },
                style={"height": "90vh", "margin-top": "1rem"},
                columnSize="autoSize",
                columnSizeOptions={
                    "keys": list(df.keys()),
                    "skipHeader": False,
                },
                dashGridOptions={
                    "rowSelection": "multiple",
                    "suppressColumnVirtualisation": True,
                    # "pagination": True,
                    # "paginationPageSize": 100,
                    # "paginationPageSizeSelector": [20, 50, 100, 500, 1000],
                },
            ),
        ]
    )

    return layout


layout = setup_all()
