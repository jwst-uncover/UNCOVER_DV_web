import pathlib
import numpy as np

import dash

from dash import html


from .utils_funcs import (
    navbar_overviews_phot,
    # _STYLES,
    _FILTERS_RGB_STR,
    _FILTERS_ALL,
    _IMGTYPES_MORPHOLOGEURS,
    _make_info_entries,
    _make_nextprev_nav,
    make_headerbar,
)

from .file_io import global_store


dash.register_page(
    __name__,
    path_template="/overviews/phot/<id>",
)

_PAGE_FLAVOR = "Phot Sample"
_VERS = "DR3"

_VERS_PHOT = "DR3"

path = pathlib.Path(__file__).parent.parent.resolve()
_FNAME_DF = f"{path}/assets/data/df_sample_phot_full.fits"
_DATA_PATH = "/assets/data/cutouts_phot/"


df = global_store(_FNAME_DF)


_DICT_KEYS = {
    "id": "id",
    "id_phot": "id",
    # "id_phot": "id_DR3",
}


_BREAKS_INFO_ENTRIES = [
    "z_phot_16",
    "mwa_16",
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


_DICT_TABLE_ENTRIES_FULL = {
    "ra": {
        "format": "0.8f",
    },
    "dec": {
        "format": "0.8f",
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
for key in _keys_flt_trim_pctl:
    for pctl in [16, 50, 84]:
        _DICT_TABLE_ENTRIES_FULL_ADD[f"{key}_{pctl}"] = {
            "format": "0.3f",
            "combine_tuple": True,
            "label_extra": " (50 [16,84])",
        }

for key in _keys_flt_trim_pctl_log:
    for pctl in [16, 50, 84]:
        _DICT_TABLE_ENTRIES_FULL_ADD[f"{key}_{pctl}"] = {
            "format": "0.2e",
            "combine_tuple": True,
            "label_extra": " (50 [16,84])",
        }


for key in _keys_flt_trim:
    _DICT_TABLE_ENTRIES_FULL_ADD[f"{key}"] = {
        "format": "0.3f",
    }


_keys_flt_trim = [
    "texp_tot",
]
for key in _keys_flt_trim:
    _DICT_TABLE_ENTRIES_FULL_ADD[f"{key}"] = {
        "format": "0.1f",
    }


_DICT_TABLE_ENTRIES_FULL.update(_DICT_TABLE_ENTRIES_FULL_ADD)


def _make_sed_sfh_entries(objid_phot):
    entries = {}

    entries_sed_sfh = []

    for fluxtype in ["fnu", "flam"]:
        entries_sed_sfh.append(
            html.Td(
                html.Img(
                    src=_DATA_PATH
                    + f"seds/DR3_{objid_phot}_sed_{fluxtype}.png",
                    alt=f"SED/{fluxtype} for {_VERS_PHOT} {objid_phot}",
                    # style={**_STYLES["plots_IMG"]},
                    className=".text-body-tertiary plots-IMG",
                ),
                # style={**_STYLES["plots"]},
                className="plots",
            )
        )
    entries_sed_sfh.append(
        html.Td(
            html.Img(
                src=_DATA_PATH + f"sfhs/DR3_{objid_phot}_SFH.png",
                alt=f"SFH for {_VERS_PHOT} {objid_phot}",
                # style={**_STYLES["plots_IMG"]},
                className=".text-body-tertiary plots-IMG",
            ),
            # style={**_STYLES["plots"]},
            className="plots",
        )
    )

    entries["sed_sfh"] = entries_sed_sfh

    return entries


def _make_rgb_segmap_entries(objid_phot):
    entries = [
        html.Td(
            html.Img(
                src=_DATA_PATH
                + f"RGB_stamps/PSF_BCG-MATCH/{objid_phot}_{filt}.png",
                alt=f"RGB {filt} postage stamp for {objid_phot}",
                # style={**_STYLES["rgb_seg_stamps_IMG"]},
                className="rgb-seg-stamps-IMG",
            ),
            # style={**_STYLES["rgb_seg_stamps"]},
            className="rgb-seg-stamps",
        )
        for filt in _FILTERS_RGB_STR
    ]

    entries.append(
        html.Td(
            html.Img(
                src=_DATA_PATH
                + f"RGB_stamps/PSF_BCG-MATCH/{objid_phot}_MB.png",
                alt=f"RGB MB postage stamp for {objid_phot}",
                # style={**_STYLES["rgb_seg_stamps_IMG"]},
                className="rgb-seg-stamps-IMG",
            ),
            # style={**_STYLES["rgb_seg_stamps"]},
            className="rgb-seg-stamps",
        )
    )

    entries.append(
        html.Td(
            html.Img(
                src=_DATA_PATH + f"segmap_stamps/{objid_phot}_segLW.png",
                alt=f"Segmap postage stamp for {objid_phot}",
                # style={**_STYLES["rgb_seg_stamps_IMG"]},
                className="rgb-seg-stamps-IMG",
            ),
            # style={**_STYLES["rgb_seg_stamps"]},
            className="rgb-seg-stamps",
        )
    )

    entries.append(
        html.Td(
            html.Img(
                src=_DATA_PATH + f"magmap_stamps/{objid_phot}_magclosest.png",
                alt=f"Magnification postage stamp for {objid_phot}",
                # style={**_STYLES["rgb_seg_stamps_IMG"]},
                className="rgb-seg-stamps-IMG",
            ),
            # style={**_STYLES["rgb_seg_stamps"]},
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
                        src=_DATA_PATH
                        + f"morph_stamps/ID_DR3_{objid_phot}_F444W_{imgtype}.png",
                        alt="",
                        # style={**_STYLES["pstamps_gallery_IMG"]},
                        className=".text-body-tertiary pstamps-gallery-IMG",
                    ),
                    # style={**_STYLES["pstamps_gallery"]},
                    className="pstamps-gallery",
                )
                for filt in _FILTERS_ALL
            ]
        else:
            entries = [
                html.Td(
                    html.Img(
                        src=_DATA_PATH
                        + f"morph_stamps/ID_DR3_{objid_phot}_{filt}_{imgtype}.png",
                        alt="",
                        # style={**_STYLES["pstamps_gallery_IMG"]},
                        className=".text-body-tertiary pstamps-gallery-IMG",
                    ),
                    # style={**_STYLES["pstamps_gallery"]},
                    className="pstamps-gallery",
                )
                for filt in _FILTERS_ALL
            ]

        entries_out = [
            html.Td(
                imgtype.capitalize(),
                # style={**_STYLES["pstamps_gallery_rowlabel"]},
                className="pstamps-gallery-rowlabel",
            ),
        ]

        entries_out.extend(entries)
    else:
        # Labels row entries:

        entries = [
            html.Td(
                filt,
                # style={**_STYLES["pstamps_gallery_collabel"]},
                className="pstamps-gallery-collabel",
            )
            for filt in _FILTERS_ALL
        ]

        entries_out = [
            html.Td(
                "",
                # style={**_STYLES["pstamps_gallery_rowlabel"]},
                className="pstamps-gallery-rowlabel",
            )
        ]
        entries_out.extend(entries)

    return entries_out


def layout(id="1.html", page_flavor=_PAGE_FLAVOR, vers=_VERS, **kwargs):
    objid_phot = np.int64(id.split(".html")[0])
    ind = np.where(df[_DICT_KEYS["id"]] == objid_phot)[0][0]

    entries_sed_sfh = _make_sed_sfh_entries(objid_phot)

    entries_rgb_segmap = _make_rgb_segmap_entries(objid_phot)

    entries_morph = {}
    for imgtype in _IMGTYPES_MORPHOLOGEURS:
        entries_morph[imgtype] = _make_morph_stamp_entries(
            objid_phot, imgtype=imgtype
        )

    entries_overview_nextprev = _make_nextprev_nav(
        df,
        ind,
        dict_keys=_DICT_KEYS,
        pathbase_link="/overviews/phot/",
    )

    entries_galprops = {}

    for jj, keys_list in enumerate(_KEYS_INFO):
        for enttype in ["labels", "entries"]:
            entries_galprops[f"{enttype}_{jj}"] = _make_info_entries(
                df,
                ind,
                dict_table_entries_full=_DICT_TABLE_ENTRIES_FULL,
                rowtype=enttype,
                keys_list=keys_list,
                key_crossref="id_spec",
                pathbase_crossref="/overviews/spec/",
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
            navbar_overviews_phot(),
            ### Galaxy properties
            html.Div(
                className="row row-mt-2",
                # style={**_STYLES["plot_divs"], "margin-top": "0.5rem"},
                children=[
                    html.Div(
                        className="column",
                        children=[
                            html.Div(
                                entries_overview_nextprev,
                                className="d-grid gap-1 d-flex navnextprev",
                            ),
                            html.Table(
                                # className="nopad",
                                className="props-table",
                                children=[
                                    html.Tr(
                                        entries_galprops[enttype],
                                        # style={**_STYLES["row_info"]},
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
                # style={**_STYLES["plot_divs"]},
                children=[
                    html.Div(
                        className="column",
                        children=[
                            html.H6("RGB images"),
                            html.Table(
                                className="nopad",
                                children=[
                                    html.Tr(
                                        entries_rgb_segmap,
                                        # style={**_STYLES["row_images"]},
                                        className="row-images",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            ### SED + SFH
            html.Div(
                className="row",
                # style={**_STYLES["plot_divs"]},
                children=[
                    html.Div(
                        className="column",
                        children=[
                            html.H6("SED + SFH"),
                            html.Table(
                                className="nopad",
                                children=[
                                    html.Tr(
                                        entries_sed_sfh[plottype],
                                        # style={**_STYLES["row_images"]},
                                        className="row-images",
                                    )
                                    for plottype in entries_sed_sfh.keys()
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            ### Morphologeurs
            html.Div(
                className="row",
                # style={**_STYLES["plot_divs"]},
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
                                        # style={**_STYLES["row_images"]},
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
