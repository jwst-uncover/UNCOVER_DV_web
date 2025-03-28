# import dash

from dash import html, dcc
import numpy as np

_FILTERS_RGB_TUPLES = [
    ["F115W+F150W", "F200W+F277W", "F356W+F410M+F444W"],
    ["F115W", "F150W", "F200W"],
    ["F277W", "F356W", "F444W"],
]

_FILTERS_ALL = [
    "F070W",
    "F090W",
    "F115W",
    "F140M",
    "F150W",
    "F162M",
    "F182M",
    "F200W",
    "F210M",
    "F250M",
    "F277W",
    "F300M",
    "F335M",
    "F356W",
    "F360M",
    "F410M",
    "F430M",
    "F444W",
    "F460M",
    "F480M",
]

_FILTERS_RGB_STR = []
for filtrgb in _FILTERS_RGB_TUPLES:
    _FILTERS_RGB_STR.append("".join(filtrgb))

_IMGTYPES_MORPHOLOGEURS = ["filt", "img", "mod", "res", "mask"]


_STYLES = {
    "plot_divs": {
        "overflowX": "auto",
        "min-width": "700px",
        "display": "flex",
    },
    "row_images": {
        "padding": "0",
        "left": "0px",
        "top": "0px",
        "position": "relative",
        "display": "flex",
        "margin": "0",
    },
    "row_info": {
        "position": "relative",
        # "display": "flex",
        # "margin": "0",
    },
    "info_entries": {
        "border": "1px solid black",
        "padding": "0.5rem",
    },
    "plots_IMG": {
        # "width": "400px",
        "height": "200px",
        "padding": "0",
        "color": "grey",
        "font-weight": "300",
    },
    "plots": {
        # "width": "400px",
        "height": "200px",
        "padding": "0.25rem",
    },
    "plots_spec_IMG": {
        "width": "1200px",
        "padding": "0",
        "color": "grey",
        "font-weight": "300",
    },
    "plots_spec": {
        "width": "1200px",
        "padding": "0.25rem",
    },
    "rgb_seg_stamps_IMG": {
        "width": "180px",
        "padding": "0",
        "color": "grey",
        "font-weight": "300",
    },
    "rgb_seg_stamps": {
        "width": "180px",
        "padding": "0.25rem",
    },
    "pstamps_gallery_IMG": {
        "width": "67px",
        "padding": "0",
        "color": "grey",
        "font-weight": "300",
    },
    "pstamps_gallery": {
        "width": "67px",
        "padding": "0",
    },
    "pstamps_gallery_rowlabel": {
        "width": "15px",
        "padding": "0",
        "writing-mode": "vertical-rl",
        "transform": "rotate(-180deg)",
        "text-align": "center",
    },
    "pstamps_gallery_collabel": {
        "width": "67px",
        "padding": "0",
        "text-align": "center",
    },
    "pre": {
        "border": "thin lightgrey solid",
        "overflowX": "auto",
        "padding": "0px 12px",
    },
    "padtop": {
        "padding-top": "100px",
    },
    "padtop_sm": {
        "padding-top": "10px",
    },
    "padtop_md": {
        "padding-top": "30px",
    },
    "bold": {
        "font-weight": "bold",
    },
}


#########################################


_DICT_OVERVIEW_ALIASES_HOME = {
    "Index phot": "Table: Full photometric sample",
    "Index spec": "Table: Spectroscopic sample",
}


_DICT_OVERVIEW_ALIASES_TABLES = {
    "Index phot": "Table: Full photometric sample",
    "Index spec": "Table: Spectroscopic sample",
}


_LIST_PAGES = [
    {
        "name": "Home",
        "relative_path": "/",
    },
    {
        "name": "Index phot",
        "relative_path": "/phot/",
    },
    {
        "name": "Index spec",
        "relative_path": "/spec/",
    },
]


def navbar_home():
    ### Links / pseudo navbar
    return html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{_DICT_OVERVIEW_ALIASES_HOME.get(page['name'], page['name'])}",
                    href=page["relative_path"],
                ),
                className="navbar",
            )
            for page in _LIST_PAGES
            if page["name"]
            in [
                "Index phot",
                "Index spec",
            ]
        ]
    )


def navbar_tables():
    return html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{_DICT_OVERVIEW_ALIASES_TABLES.get(page['name'], page['name'])}",
                    href=page["relative_path"],
                ),
                className="navbar_small",
            )
            for page in _LIST_PAGES
            if page["name"]
            in [
                "Home",
            ]
        ]
    )


def navbar_overviews_spec():
    return html.Div(
        [
            html.Div(
                [
                    dcc.Link(
                        f"{_DICT_OVERVIEW_ALIASES_TABLES.get(page['name'], page['name'])}",
                        href=page["relative_path"],
                    )
                    for page in _LIST_PAGES
                    if page["name"]
                    in [
                        "Home",
                        "Index spec",
                    ]
                ],
                className="navbar_small navbarhoriz",
            ),
        ]
    )


def navbar_overviews_phot():
    return html.Div(
        [
            html.Div(
                [
                    dcc.Link(
                        f"{_DICT_OVERVIEW_ALIASES_TABLES.get(page['name'], page['name'])}",
                        href=page["relative_path"],
                    )
                    for page in _LIST_PAGES
                    if page["name"]
                    in [
                        "Home",
                        "Index phot",
                    ]
                ],
                className="navbar_small navbarhoriz",
            ),
        ]
    )


def _make_info_entry(val, style_kwargs={}):
    return html.Td(
        val,
        style={**_STYLES["info_entries"], **style_kwargs},
    )


def _make_info_entry_link(
    val,
    pathbase=None,
):
    if isinstance(val, np.ma.core.MaskedConstant):
        entry = _make_info_entry(val)
    elif val == -9999:
        entry = _make_info_entry(val)
    else:
        entry = html.Td(
            dcc.Link(
                val,
                href=f"{pathbase}{int(val)}.html",
            ),
            style={**_STYLES["info_entries"]},
        )
    return entry


def _make_info_entries(
    df,
    ind,
    dict_table_entries_full=None,
    rowtype="labels",
    keys_list=None,
    key_crossref=None,
    pathbase_crossref=None,
):
    if rowtype == "labels":
        entries = []
        for key in keys_list:
            combine_tuple = False
            if key in dict_table_entries_full.keys():
                combine_tuple = dict_table_entries_full[key].get(
                    "combine_tuple", False
                )
            if combine_tuple:
                if key.split("_")[-1] == "50":
                    lbl = "_".join(key.split("_")[:-1])
                    lbl += dict_table_entries_full[key].get("label_extra", "")
                    entries.append(
                        _make_info_entry(
                            lbl, style_kwargs={"font-weight": "600"}
                        )
                    )
            else:
                entries.append(
                    _make_info_entry(key, style_kwargs={"font-weight": "600"})
                )

    elif rowtype == "entries":
        entries = []

        for key in keys_list:
            fmt = None
            if key in dict_table_entries_full.keys():
                fmt = dict_table_entries_full[key].get("format", None)

            combine_tuple = False
            if key in dict_table_entries_full.keys():
                combine_tuple = dict_table_entries_full[key].get(
                    "combine_tuple", False
                )
            if combine_tuple:
                if key.split("_")[-1] == "50":
                    keybase = "_".join(key.split("_")[:-1])

                    if fmt is not None:
                        val50 = f"{df[keybase + '_50'][ind]:{fmt}}"
                        val16 = f"{df[keybase + '_16'][ind]:{fmt}}"
                        val84 = f"{df[keybase + '_84'][ind]:{fmt}}"
                        val = f"{val50} [{val16}, {val84}]"
                    else:
                        val50 = f"{df[keybase + '_50'][ind]}"
                        val16 = f"{df[keybase + '_16'][ind]}"
                        val84 = f"{df[keybase + '_84'][ind]}"
                        val = f"{val50} [{val16}, {val84}]"
                else:
                    val = None

            else:
                if fmt is not None:
                    val = f"{df[key][ind]:{fmt}}"
                else:
                    val = df[key][ind]

            if val is not None:
                if key == key_crossref:
                    entries.append(
                        _make_info_entry_link(val, pathbase=pathbase_crossref)
                    )

                else:
                    entries.append(_make_info_entry(val))

    else:
        raise ValueError

    return entries
