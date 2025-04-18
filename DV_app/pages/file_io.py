import dash
import os
import pathlib
import numpy as np

from flask_caching import Cache

from astropy.table import Table, MaskedColumn


import warnings
from astropy.units import UnitsWarning

warnings.simplefilter("ignore", category=UnitsWarning)


def make_column_defs(dict_table_entries):
    columnDefs = []

    for keyin in dict_table_entries:
        key = keyin

        dict_col = {
            "field": key,
            "headerName": dict_table_entries[keyin].get("header", key),
        }
        fmt = dict_table_entries[keyin].get("format", None)
        if fmt is not None:
            dict_col["valueFormatter"] = {
                "function": f"params.value ? d3.format('{fmt}')(params.value): '' "
            }

        renderer = dict_table_entries[keyin].get("cellRenderer", None)
        if renderer is not None:
            dict_col["cellRenderer"] = renderer

        columnDefs.append(dict_col)

    return columnDefs


def get_table(fname_DF):
    splt = fname_DF.split(".")[0].split("_")

    df = Table.read(fname_DF)

    if "id_msa_epoch1" in df.keys():
        df = _clean_null_IDs(
            df, keys=["id_DR3", "id_msa_epoch1", "id_msa_epoch2"]
        )

    if splt[-1] == "index":
        df = df.to_pandas()

    return df


def _clean_null_IDs(df, keys=None, badval=-9999):
    for key in keys:
        df[key] = np.array(df[key], dtype=np.float64)

        df[key][(df[key] == badval)] = np.nan
        # df.loc[(df[key] == badval), key] = np.nan

        df[key] = MaskedColumn(
            df[key],
            name=key,
            mask=(~np.isfinite(df[key])),
            dtype=df[key].dtype,
        )

    return df


# def global_store(value):
#     return get_table(value)


REDIS_HOST = os.environ.get("REDIS_HOST", "0.0.0.0")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")


app = dash.get_app()
CACHE_CONFIG = {
    # "CACHE_TYPE": "SimpleCache",  ## DEBUGGING
    "CACHE_TYPE": "redis",
    "CACHE_REDIS_URL": f"redis://{REDIS_HOST}:{REDIS_PORT}",
}
cache = Cache(
    app.server,
    config=CACHE_CONFIG,
)


# cached to redis memory store to share between pages
@cache.memoize()
def global_store(value):
    df = get_table(value)
    return df


def preload_all_data():
    path = pathlib.Path(__file__).parent.parent.resolve()
    _FNAME_DF_PHOT_INDEX = f"{path}/assets/data/df_sample_phot_index.fits"
    _FNAME_DF_SPEC_INDEX = f"{path}/assets/data/df_sample_spec_index.fits"
    _FNAME_DF_PHOT_FULL = f"{path}/assets/data/df_sample_phot_full.fits"
    _FNAME_DF_SPEC_FULL = f"{path}/assets/data/df_sample_spec_full.fits"

    _ = global_store(_FNAME_DF_PHOT_INDEX)
    _ = global_store(_FNAME_DF_SPEC_INDEX)
    _ = global_store(_FNAME_DF_PHOT_FULL)
    _ = global_store(_FNAME_DF_SPEC_FULL)

    return None
