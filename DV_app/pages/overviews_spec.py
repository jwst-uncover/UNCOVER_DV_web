import pathlib
import numpy as np

import dash

from dash import html

from .utils_funcs import (
    navbar_overviews_spec,
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
    path_template="/overviews/spec/<id>",
)


_PAGE_FLAVOR = "Spec Sample"
_VERS = "v1.3"

_VERS_PHOT = "DR3"

path = pathlib.Path(__file__).parent.parent.resolve()
_FNAME_DF = f"{path}/assets/data/df_sample_spec_full.fits"
_DATA_PATH_SPEC = "/assets/data/cutouts_spec/"
_DATA_PATH_PHOT = "/assets/data/cutouts_phot/"


df = global_store(_FNAME_DF)


_DICT_KEYS = {
    "id": "specid",
    "id_phot": "id_DR3",
}


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
            _DICT_TABLE_ENTRIES_FULL_ADD[f"{key}_{pctl}"]["label_alt"] = dkey

for key in _keys_flt_trim_pctl_log:
    dkey = _dict_keys_alt_names.get(key, None)
    for pctl in [16, 50, 84]:
        _DICT_TABLE_ENTRIES_FULL_ADD[f"{key}_{pctl}"] = {
            "format": "0.2e",
            "combine_tuple": True,
            "label_extra": " (50 [16,84])",
        }
        if dkey is not None:
            _DICT_TABLE_ENTRIES_FULL_ADD[f"{key}_{pctl}"]["label_alt"] = dkey

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


def _make_spec_entries(objid, alt=False):
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
                + f"spectra/specid_{objid}_spec{extra}.png",
                alt=f"Spectrum for {objid}{extra_alttext}",
                className=f".text-body-tertiary {class_img}",
            ),
            className=f"{class_td}",
        )
    ]

    return entries


def _make_sed_sfh_pz_entries(objid, objid_phot):
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
                src=_DATA_PATH_SPEC + f"Pzs/specid_{objid:03}_Pz.png",
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


def layout(id="1.html", page_flavor=_PAGE_FLAVOR, vers=_VERS, **kwargs):
    objid = np.int64(id.split(".html")[0])

    ind = np.where(df[_DICT_KEYS["id"]] == objid)[0][0]

    objid_phot = np.int64(df[_DICT_KEYS["id_phot"]][ind])

    entries_spec = _make_spec_entries(objid)

    entries_spec_alt = _make_spec_entries(objid, alt=True)

    entries_sed_sfh_pz = _make_sed_sfh_pz_entries(objid, objid_phot)

    entries_rgb_segmap = _make_rgb_segmap_entries(objid)

    entries_morph = {}
    for imgtype in _IMGTYPES_MORPHOLOGEURS:
        entries_morph[imgtype] = _make_morph_stamp_entries(
            objid_phot, imgtype=imgtype
        )

    entries_overview_nextprev = _make_nextprev_nav(
        df,
        ind,
        dict_keys=_DICT_KEYS,
        pathbase_link="/overviews/spec/",
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
            navbar_overviews_spec(),
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
