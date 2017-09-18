"""
API Errors module provides a view of full set of errors that can be thrown
to API user.

WARNING: A set of API errors and other values are loaded in runtime, on the
first import of this module.
"""
import json
import os
import types

import dpl

config_path = os.path.join(dpl.DPL_INSTALL_PATH, "internal_config", "api_errors.json")

data = {}

with open(config_path) as f:
    data.update(json.load(f))

DOC_BASE_URL = data.get("docs_base_url", None)


class ApiError(object):
    def __init__(self, error_id: int, devel_message: str = None, user_message: str = None):
        if user_message is None:
            user_message = devel_message

        self._id = error_id
        self._devel_message = devel_message
        self._user_message = user_message
        self._docs_url = DOC_BASE_URL + str(error_id)

    @property
    def error_id(self) -> int:
        return self._id

    @property
    def devel_message(self) -> str:
        return self._devel_message

    @property
    def user_message(self) -> str:
        return self._user_message

    @property
    def docs_url(self) -> str:
        return self._docs_url

    def to_dict(self) -> dict:
        return {
            "error_id": self.error_id,
            "devel_message": self.devel_message,
            "user_message": self.user_message,
            "docs_url": self.docs_url
        }

_error_templates = {}

for item in data["errors"]:
    error_id = item["error_id"]

    _error_templates[error_id] = ApiError(**item)

ERROR_TEMPLATES = types.MappingProxyType(_error_templates)  # type: types.MappingProxyType[int, ApiError]
