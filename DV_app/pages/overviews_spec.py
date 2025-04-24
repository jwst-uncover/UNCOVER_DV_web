import dash

from .file_io import (
    _FNAME_DF_SPEC_FULL,
    _VERS_SPEC,
)
from .utils_funcs import setup_layout_spec_overview, _PAGE_FLAVOR_SPEC_OVERVIEW

_SPEC_PATH_EXTRA = ""

dash.register_page(
    __name__,
    path_template=f"/overviews/spec{_SPEC_PATH_EXTRA}/<id>",
)


def layout(
    id="1.html",
    page_flavor=_PAGE_FLAVOR_SPEC_OVERVIEW,
    vers=_VERS_SPEC,
    fname_DF=_FNAME_DF_SPEC_FULL,
    spec_path_extra=_SPEC_PATH_EXTRA,
    **kwargs,
):
    return setup_layout_spec_overview(
        id=id,
        page_flavor=page_flavor,
        vers=vers,
        fname_DF=fname_DF,
        spec_path_extra=spec_path_extra,
        **kwargs,
    )
