import pathlib

import dash
import dash_ag_grid as dag
from dash import html

from .utils_funcs import navbar_tables

from .file_io import global_store, make_column_defs

_PAGE_FLAVOR = "Spec Sample"
_VERS = "v1.3"


_DICT_TABLE_ENTRIES = {
    "specid": {
        # "header": "specid",
        "cellRenderer": "OverviewSpecLink",
        "format": "d",
    },
    "id_DR3": {
        "cellRenderer": "OverviewPhotLink",
        "format": "d",
    },
    "z_spec": {
        "format": "0.3f",
    },
    ####
    "magF444W": {
        "format": "0.2f",
    },
    "z_phot_50": {
        "from": "sps",
        "format": "0.3f",
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
    ####
    "ra": {
        "format": "0.8f",
    },
    "dec": {
        "format": "0.8f",
    },
    "id_msa_epoch1": {
        "format": "d",
    },
    "id_msa_epoch2": {
        "format": "d",
    },
    "sep_DR3_epoch1": {
        "format": "0.3f",
    },
    "sep_DR3_epoch2": {
        "format": "0.3f",
    },
}
for i in range(1, 10):
    _DICT_TABLE_ENTRIES[f"mask{i}"] = {}


path = pathlib.Path(__file__).parent.parent.resolve()
_FNAME_DF = f"{path}/assets/data/df_sample_spec_index.fits"


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
        path="/spec/",
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
