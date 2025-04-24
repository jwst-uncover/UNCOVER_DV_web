import dash_ag_grid as dag

from dash import html, dcc
import dash_bootstrap_components as dbc
import numpy as np

from .file_io import (
    global_store,
    make_column_defs,
    _VERS_SPEC,
    _VERS_SPEC_PREV,
    _VERS_PHOT,
    _FNAME_DF_SPEC_INDEX,
    _FNAME_DF_SPEC_FULL,
)


_PAGE_FLAVOR_SPEC_INDEX = "Spec Sample"
_SPEC_PATH_EXTRA = f"_{_VERS_SPEC}"


_PAGE_FLAVOR_SPEC_OVERVIEW = "Spec Sample"

_DATA_PATH_SPEC = "/assets/data/cutouts_spec/"
_DATA_PATH_PHOT = "/assets/data/cutouts_phot/"


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

_DAG_STYLE = {
    "height": "90vh",
    "margin-top": "1rem",
}


###########################################################################


_DICT_OVERVIEW_ALIASES = {
    "Index phot": "Table: Full photometric sample",
    "Index spec": "Table: Spectroscopic sample",
    "Index spec prev": f"Table: Spectroscopic sample ({_VERS_SPEC_PREV})",
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
    {
        "name": "Index spec prev",
        "relative_path": f"/spec_{_VERS_SPEC_PREV}/",
    },
]

theme_toggler = dbc.DropdownMenu(
    [
        dbc.DropdownMenuItem(
            [
                html.I(className="bi bi-sun-fill"),
                "Light",
            ],
            id="select-light",
        ),
        dbc.DropdownMenuItem(
            [
                html.I(className="bi bi-moon-fill"),
                "Dark",
            ],
            id="select-dark",
        ),
        dbc.DropdownMenuItem(
            [
                html.I(className="bi bi-circle-half"),
                "Auto",
            ],
            active=True,
            id="select-auto",
        ),
    ],
    label=[
        html.I(
            className="bi bi-circle-half",
            id="theme-icon-active",
        ),
        html.Span(
            "Toggle theme",
            id="bd-theme-text",
            className="d-none ms-2",
        ),
    ],
    id="bd-theme",
)


def make_headerbar(h2_entry=None):
    headerbar = [
        html.Ul(
            [
                html.Li(
                    html.H2(
                        children=h2_entry,
                    ),
                    id="heading-text",
                ),
                html.Li(
                    theme_toggler,
                    id="theme-toggler",
                ),
            ],
            className="header-bar",
        ),
        html.Div(
            id="bd-theme-on-load",
        ),
        html.Div(
            id="bd-theme-on-load-output",
        ),
    ]

    return headerbar


def navbar_home():
    ### Links / pseudo navbar
    return html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{_DICT_OVERVIEW_ALIASES.get(page['name'], page['name'])}",
                    href=page["relative_path"],
                ),
                className="navbar",
            )
            for page in _LIST_PAGES
            if page["name"]
            in [
                "Index phot",
                "Index spec",
                "Index spec prev",
            ]
        ]
    )


def navbar_tables():
    return html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{_DICT_OVERVIEW_ALIASES.get(page['name'], page['name'])}",
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


def navbar_overviews_spec(vers=_VERS_SPEC):
    if vers != _VERS_SPEC:
        name_ext = " prev"
    else:
        name_ext = ""

    return html.Div(
        [
            html.Div(
                [
                    dcc.Link(
                        f"{_DICT_OVERVIEW_ALIASES.get(page['name'], page['name'])}",
                        href=page["relative_path"],
                    )
                    for page in _LIST_PAGES
                    if page["name"]
                    in [
                        "Home",
                        f"Index spec{name_ext}",
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
                        f"{_DICT_OVERVIEW_ALIASES.get(page['name'], page['name'])}",
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


def _make_info_entry(val, className=None):
    return html.Td(
        val,
        className=className,
    )


def _make_info_entry_link(
    val,
    pathbase=None,
    className=None,
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
            className=className,
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
                    # lbl = "_".join(key.split("_")[:-1])
                    lbl = dict_table_entries_full[key].get(
                        "label_alt", "_".join(key.split("_")[:-1])
                    )
                    lbl += dict_table_entries_full[key].get("label_extra", "")

                else:
                    lbl = None
            else:
                # lbl = key
                entry = dict_table_entries_full.get("key", None)
                if entry is not None:
                    lbl = dict_table_entries_full[key].get("label_alt", key)
                else:
                    lbl = key

            if lbl is not None:
                entries.append(
                    _make_info_entry(
                        lbl,
                        className="info-label",
                    )
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


def _make_nextprev_nav(df, ind, dict_keys=None, pathbase_link=None):
    objid = df[dict_keys["id"]][ind]

    objid_p = None
    objid_n = None
    if ind > 0:
        objid_p = df[dict_keys["id"]][ind - 1]

    if ind < (len(df) - 1):
        objid_n = df[dict_keys["id"]][ind + 1]

    entries = [
        html.H5(
            f"Overview: {objid}",
            className="me-1",
        )
    ]

    if objid_p is not None:
        entries.append(
            dbc.Button(
                f"Prev: {objid_p}",
                href=f"{pathbase_link}{objid_p}.html",
                color="primary",
                outline=True,
                className="me-1 ms-3",
            )
        )
    else:
        entries.append(
            dbc.Button(
                "Prev",
                color="primary",
                outline=True,
                disabled=True,
                className="me-1 ms-3",
            )
        )
    if objid_n is not None:
        entries.append(
            dbc.Button(
                f"Next: {objid_n}",
                href=f"{pathbase_link}{objid_n}.html",
                color="primary",
                outline=True,
                className="me-1",
            )
        )
    else:
        entries.append(
            dbc.Button(
                "Next",
                color="primary",
                outline=True,
                disabled=True,
                className="me-1",
            )
        )

    return entries


###########################################################################


def _make_dict_table_entries_index_spec(vers=_VERS_SPEC):
    if vers != _VERS_SPEC:
        cellRendererParams = {"path_extra": f"_{vers}"}
    else:
        cellRendererParams = {"path_extra": ""}

    _DICT_TABLE_ENTRIES_INDEX_SPEC = {
        "specid": {
            "cellRenderer": "OverviewSpecLink",
            "cellRendererParams": cellRendererParams,
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
        _DICT_TABLE_ENTRIES_INDEX_SPEC[f"mask{i}"] = {}

    return _DICT_TABLE_ENTRIES_INDEX_SPEC


def setup_all_spec_index(
    page_flavor=_PAGE_FLAVOR_SPEC_INDEX,
    vers=_VERS_SPEC,
    fname_DF=_FNAME_DF_SPEC_INDEX,
    spec_path_extra=_SPEC_PATH_EXTRA,
):
    dict_table_entries = _make_dict_table_entries_index_spec(vers=vers)
    columnDefs = make_column_defs(dict_table_entries)
    df = global_store(fname_DF)

    # dash.register_page(
    #     __name__,
    #     path=f"/spec{spec_path_extra}/",
    #     title=f"UNCOVER Data Viewer: {page_flavor} {vers}",
    # )

    headerbar = make_headerbar(
        h2_entry=[
            html.A(
                "UNCOVER",
                href="https://jwst-uncover.github.io",
            ),
            f" Data Viewer: {page_flavor} {vers}",
        ]
    )

    layout = html.Div(
        [
            html.Div(
                headerbar,
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
                style=_DAG_STYLE,
                columnSize="autoSize",
                columnSizeOptions={
                    "keys": list(df.keys()),
                    "skipHeader": False,
                },
                dashGridOptions={
                    "rowSelection": "multiple",
                    "suppressColumnVirtualisation": True,
                },
                className="ag-theme-quartz dbc-ag-grid",
            ),
        ]
    )

    return layout


###########################################################################


def _make_dict_keys_overview_spec():
    _DICT_KEYS = {
        "id": "specid",
        "id_phot": "id_DR3",
    }
    return _DICT_KEYS


def _make_keys_info_overview_spec(df):
    _BREAKS_INFO_ENTRIES = [
        "ra",
        "z_phot_16",
    ]
    _KEYS_INFO = []

    _indstart = 0
    _keys_orig = np.array(list(df.keys()))
    for bkey in _BREAKS_INFO_ENTRIES:
        whkey = np.where(_keys_orig == bkey)[0]
        _indend = whkey[0]
        _KEYS_INFO.append(_keys_orig[_indstart:_indend])
        _indstart = _indend
    _KEYS_INFO.append(_keys_orig[_indstart:])
    return _KEYS_INFO


def _make_dict_table_entries_full_spec():
    _DICT_TABLE_ENTRIES_FULL = {
        "ra": {
            "format": "0.8f",
        },
        "dec": {
            "format": "0.8f",
        },
        "sep_DR3_epoch1": {
            "format": "0.3f",
        },
        "sep_DR3_epoch2": {
            "format": "0.3f",
        },
    }

    _DICT_TABLE_ENTRIES_FULL_ADD = {
        "magF444W": {
            "format": "0.3f",
        },
    }

    _keys_flt_trim_pctl = [
        "z_phot",
        "mu",
        "lmstar",
        "mwa",
        "dust2",
        "lmet",
        "logfagn",
        "z_spec",  # to get _16,_50,_84
    ]
    _keys_flt_trim_pctl_log = [
        "sfr100",
        "ssfr100",
    ]
    _keys_flt_trim = [
        "z_spec",
    ]

    _dict_keys_alt_names = {
        "z_phot": "z_SPS",
    }

    for key in _keys_flt_trim_pctl:
        dkey = _dict_keys_alt_names.get(key, None)
        for pctl in [16, 50, 84]:
            _DICT_TABLE_ENTRIES_FULL_ADD[f"{key}_{pctl}"] = {
                "format": "0.3f",
                "combine_tuple": True,
                "label_extra": " (50 [16,84])",
            }
            if dkey is not None:
                _DICT_TABLE_ENTRIES_FULL_ADD[f"{key}_{pctl}"]["label_alt"] = (
                    dkey
                )

    for key in _keys_flt_trim_pctl_log:
        dkey = _dict_keys_alt_names.get(key, None)
        for pctl in [16, 50, 84]:
            _DICT_TABLE_ENTRIES_FULL_ADD[f"{key}_{pctl}"] = {
                "format": "0.2e",
                "combine_tuple": True,
                "label_extra": " (50 [16,84])",
            }
            if dkey is not None:
                _DICT_TABLE_ENTRIES_FULL_ADD[f"{key}_{pctl}"]["label_alt"] = (
                    dkey
                )

    for key in _keys_flt_trim:
        dkey = _dict_keys_alt_names.get(key, None)
        _DICT_TABLE_ENTRIES_FULL_ADD[f"{key}"] = {
            "format": "0.3f",
        }

        if dkey is not None:
            _DICT_TABLE_ENTRIES_FULL_ADD[f"{key}"]["label_alt"] = dkey

    _keys_flt_trim = [
        "texp_tot",
    ]
    for key in _keys_flt_trim:
        _DICT_TABLE_ENTRIES_FULL_ADD[f"{key}"] = {
            "format": "0.1f",
        }

    _DICT_TABLE_ENTRIES_FULL.update(_DICT_TABLE_ENTRIES_FULL_ADD)

    return _DICT_TABLE_ENTRIES_FULL


def _make_spec_entries(objid, spec_path_extra=None, alt=False):
    entries = {}

    class_img = "plots-spec-IMG"
    class_td = "plots-spec"
    extra = ""
    extra_alttext = ""

    if alt:
        extra = "_alt"
        extra_alttext = ", alternative background subtraction"
        class_img += "-alt"
        class_td += "-alt"

    entries["spec"] = [
        html.Td(
            html.Img(
                src=_DATA_PATH_SPEC
                + f"spectra{spec_path_extra}/specid_{objid}_spec{extra}.png",
                alt=f"Spectrum for {objid}{extra_alttext}",
                className=f".text-body-tertiary {class_img}",
            ),
            className=f"{class_td}",
        )
    ]

    return entries


def _make_sed_sfh_pz_entries(objid, objid_phot, spec_path_extra=None):
    entries = {}

    entries_sed_sfh_pz = []

    for fluxtype in ["fnu", "flam"]:
        entries_sed_sfh_pz.append(
            html.Td(
                html.Img(
                    src=_DATA_PATH_PHOT
                    + f"seds/DR3_{objid_phot}_sed_{fluxtype}.png",
                    alt=f"SED/{fluxtype} for {objid}/ {_VERS_PHOT} {objid_phot}",
                    className=".text-body-tertiary plots-IMG",
                ),
                className="plots",
            )
        )
    entries_sed_sfh_pz.append(
        html.Td(
            html.Img(
                src=_DATA_PATH_PHOT + f"sfhs/DR3_{objid_phot}_SFH.png",
                alt=f"SFH for {objid}/ {_VERS_PHOT} {objid_phot}",
                className=".text-body-tertiary plots-IMG",
            ),
            className="plots",
        )
    )
    entries_sed_sfh_pz.append(
        html.Td(
            html.Img(
                src=_DATA_PATH_SPEC
                + f"Pzs{spec_path_extra}/specid_{objid:03}_Pz.png",
                alt=f"P(z) for {objid}/ {_VERS_PHOT} {objid_phot}",
                className=".text-body-tertiary plots-IMG",
            ),
            className="plots",
        )
    )

    entries["sed_sfh_pz"] = entries_sed_sfh_pz

    return entries


def _make_rgb_segmap_entries(objid):
    entries = [
        html.Td(
            html.Img(
                src=_DATA_PATH_SPEC
                + f"RGB_stamps/PSF_BCG-MATCH/{objid}_{filt}.png",
                alt=f"RGB {filt} postage stamp for {objid}",
                className=".text-body-tertiary rgb-seg-stamps-IMG",
            ),
            className="rgb-seg-stamps",
        )
        for filt in _FILTERS_RGB_STR
    ]

    entries.append(
        html.Td(
            html.Img(
                src=_DATA_PATH_SPEC
                + f"RGB_stamps/PSF_BCG-MATCH/{objid}_MB.png",
                alt=f"RGB MB postage stamp for {objid}",
                className=".text-body-tertiary rgb-seg-stamps-IMG",
            ),
            className="rgb-seg-stamps",
        )
    )

    entries.append(
        html.Td(
            html.Img(
                src=_DATA_PATH_SPEC + f"segmap_stamps/{objid}_segLW.png",
                alt=f"Segmap postage stamp for {objid}",
                className=".text-body-tertiary rgb-seg-stamps-IMG",
            ),
            className="rgb-seg-stamps",
        )
    )

    entries.append(
        html.Td(
            html.Img(
                src=_DATA_PATH_SPEC + f"magmap_stamps/{objid}_magclosest.png",
                alt=f"Magnification postage stamp for {objid}",
                className=".text-body-tertiary rgb-seg-stamps-IMG",
            ),
            className="rgb-seg-stamps",
        )
    )

    entries.append(
        html.Td(
            html.Img(
                src=_DATA_PATH_SPEC
                + f"msa_shutter_stamps/{objid}_F444W_slitlets.png",
                alt=f"Shutter postage stamp for {objid}",
                className=".text-body-tertiary rgb-seg-stamps-IMG",
            ),
            className="rgb-seg-stamps",
        )
    )

    return entries


def _make_morph_stamp_entries(objid_phot, imgtype="img"):
    if imgtype in _IMGTYPES_MORPHOLOGEURS[1:]:
        if imgtype == "mask":
            entries = [
                html.Td(
                    html.Img(
                        src=_DATA_PATH_PHOT
                        + f"morph_stamps/ID_DR3_{objid_phot}_F444W_{imgtype}.png",
                        alt="",
                        className=".text-body-tertiary pstamps-gallery-IMG",
                    ),
                    className="pstamps-gallery",
                )
                for filt in _FILTERS_ALL
            ]
        else:
            entries = [
                html.Td(
                    html.Img(
                        src=_DATA_PATH_PHOT
                        + f"morph_stamps/ID_DR3_{objid_phot}_{filt}_{imgtype}.png",
                        alt="",
                        className=".text-body-tertiary pstamps-gallery-IMG",
                    ),
                    className="pstamps-gallery",
                )
                for filt in _FILTERS_ALL
            ]

        entries_out = [
            html.Td(
                imgtype.capitalize(),
                className="pstamps-gallery-rowlabel",
            ),
        ]

        entries_out.extend(entries)
    else:
        # Labels row entries:
        entries = [
            html.Td(
                filt,
                className="pstamps-gallery-collabel",
            )
            for filt in _FILTERS_ALL
        ]

        entries_out = [html.Td("", className="pstamps-gallery-rowlabel")]
        entries_out.extend(entries)

    return entries_out


def setup_layout_spec_overview(
    id="1.html",
    page_flavor=_PAGE_FLAVOR_SPEC_OVERVIEW,
    vers=_VERS_SPEC,
    fname_DF=_FNAME_DF_SPEC_FULL,
    spec_path_extra=_SPEC_PATH_EXTRA,
    dict_keys=_make_dict_keys_overview_spec(),
    dict_table_entries_full=_make_dict_table_entries_full_spec(),
    **kwargs,
):
    # dash.register_page(
    #     __name__,
    #     path_template=f"/overviews/spec{spec_path_extra}/<id>",
    # )

    df = global_store(fname_DF)

    # def layout(id="1.html", page_flavor=_PAGE_FLAVOR, vers=_VERS, **kwargs):
    objid = np.int64(id.split(".html")[0])

    ind = np.where(df[dict_keys["id"]] == objid)[0][0]

    objid_phot = np.int64(df[dict_keys["id_phot"]][ind])

    entries_spec = _make_spec_entries(objid, spec_path_extra=spec_path_extra)

    entries_spec_alt = _make_spec_entries(
        objid, alt=True, spec_path_extra=spec_path_extra
    )

    entries_sed_sfh_pz = _make_sed_sfh_pz_entries(
        objid, objid_phot, spec_path_extra=spec_path_extra
    )

    entries_rgb_segmap = _make_rgb_segmap_entries(objid)

    entries_morph = {}
    for imgtype in _IMGTYPES_MORPHOLOGEURS:
        entries_morph[imgtype] = _make_morph_stamp_entries(
            objid_phot, imgtype=imgtype
        )

    entries_overview_nextprev = _make_nextprev_nav(
        df,
        ind,
        dict_keys=dict_keys,
        pathbase_link=f"/overviews/spec{spec_path_extra}/",
    )

    entries_galprops = {}

    keys_info = _make_keys_info_overview_spec(df)

    for jj, keys_list in enumerate(keys_info):
        for enttype in ["labels", "entries"]:
            entries_galprops[f"{enttype}_{jj}"] = _make_info_entries(
                df,
                ind,
                dict_table_entries_full=dict_table_entries_full,
                rowtype=enttype,
                keys_list=keys_list,
                key_crossref="id_DR3",
                pathbase_crossref="/overviews/phot/",
            )

    headerbar = make_headerbar(
        h2_entry=[
            html.A(
                "UNCOVER",
                href="https://jwst-uncover.github.io",
            ),
            f" Data Viewer: {page_flavor} {vers}",
        ]
    )

    overviewlayout = html.Div(
        [
            html.Div(
                headerbar,
            ),
            ### Links / pseudo navbar
            navbar_overviews_spec(vers=vers),
            ### Galaxy properties
            html.Div(
                className="row row-mt-2",
                children=[
                    html.Div(
                        className="column",
                        children=[
                            html.Div(
                                entries_overview_nextprev,
                                className="d-grid gap-1 d-flex navnextprev",
                            ),
                            html.Table(
                                className="props-table",
                                children=[
                                    html.Tr(
                                        entries_galprops[enttype],
                                    )
                                    for enttype in entries_galprops.keys()
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            ### RGB stamps + segmap
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="column",
                        children=[
                            html.H6(
                                "RGB images + Segmap + Magmap + Shuttermap "
                            ),
                            html.Table(
                                className="nopad",
                                children=[
                                    html.Tr(
                                        entries_rgb_segmap,
                                        className="row-images",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            ### Spectrum
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="column",
                        children=[
                            html.H6("Spectrum"),
                            html.Table(
                                className="nopad",
                                children=[
                                    html.Tr(
                                        entries_spec[plottype],
                                        className="row-images",
                                    )
                                    for plottype in entries_spec.keys()
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            ### Spectrum: alternative background subtraction
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="column",
                        children=[
                            html.Table(
                                className="nopad",
                                children=[
                                    html.Tr(
                                        entries_spec_alt[plottype],
                                        className="row-images",
                                    )
                                    for plottype in entries_spec_alt.keys()
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            ### SED + SFH + p(z)
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="column",
                        children=[
                            html.H6("SED + SFH + p(z)"),
                            html.Table(
                                className="nopad",
                                children=[
                                    html.Tr(
                                        entries_sed_sfh_pz[plottype],
                                        className="row-images",
                                    )
                                    for plottype in entries_sed_sfh_pz.keys()
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            ### Morphologeurs
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="column",
                        children=[
                            html.H6("Morphologeurs"),
                            html.Table(
                                className="nopad",
                                children=[
                                    html.Tr(
                                        entries_morph[imgtype],
                                        className="row-images",
                                    )
                                    for imgtype in entries_morph.keys()
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            ###
        ]
    )

    return overviewlayout


###########################################################################
