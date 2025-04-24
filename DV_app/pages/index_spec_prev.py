import dash
from .file_io import (
    _FNAME_DF_SPEC_INDEX_PREV,
    _VERS_SPEC_PREV,
    _INCLUDE_PREV,
)

from .utils_funcs import setup_all_spec_index, _PAGE_FLAVOR_SPEC_INDEX


if _INCLUDE_PREV:
    _VERS = _VERS_SPEC_PREV
    _SPEC_PATH_EXTRA = f"_{_VERS_SPEC_PREV}"

    dash.register_page(
        __name__,
        path=f"/spec{_SPEC_PATH_EXTRA}/",
        title=f"UNCOVER Data Viewer: {_PAGE_FLAVOR_SPEC_INDEX} {_VERS}",
    )

    layout = setup_all_spec_index(
        vers=_VERS,
        fname_DF=_FNAME_DF_SPEC_INDEX_PREV,
        spec_path_extra=_SPEC_PATH_EXTRA,
    )
