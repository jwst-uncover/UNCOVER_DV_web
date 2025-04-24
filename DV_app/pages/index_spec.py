import dash
from .file_io import (
    _FNAME_DF_SPEC_INDEX,
    _VERS_SPEC,
)

from .utils_funcs import setup_all_spec_index, _PAGE_FLAVOR_SPEC_INDEX

_VERS = _VERS_SPEC
_SPEC_PATH_EXTRA = ""


dash.register_page(
    __name__,
    path=f"/spec{_SPEC_PATH_EXTRA}/",
    title=f"UNCOVER Data Viewer: {_PAGE_FLAVOR_SPEC_INDEX} {_VERS}",
)

layout = setup_all_spec_index(
    vers=_VERS,
    fname_DF=_FNAME_DF_SPEC_INDEX,
    spec_path_extra=_SPEC_PATH_EXTRA,
)
