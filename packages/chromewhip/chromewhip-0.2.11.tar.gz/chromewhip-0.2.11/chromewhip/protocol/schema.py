# noinspection PyPep8
# noinspection PyArgumentList

"""
AUTO-GENERATED BY `scripts/generate_protocol.py` using `data/browser_protocol.json`
and `data/js_protocol.json` as inputs! Please do not modify this file.
"""

import logging
from typing import Any, Optional, Union

from chromewhip.helpers import PayloadMixin, BaseEvent, ChromeTypeBase

log = logging.getLogger(__name__)

# Domain: Description of the protocol domain.
class Domain(ChromeTypeBase):
    def __init__(self,
                 name: Union['str'],
                 version: Union['str'],
                 ):

        self.name = name
        self.version = version


class Schema(PayloadMixin):
    """ This domain is deprecated.
    """
    @classmethod
    def getDomains(cls):
        """Returns supported domains.
        """
        return (
            cls.build_send_payload("getDomains", {
            }),
            cls.convert_payload({
                "domains": {
                    "class": [Domain],
                    "optional": False
                },
            })
        )

