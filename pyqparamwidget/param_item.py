"""
Parameter Item

.. autosummary::
   ~ParameterItem
"""

__all__ = ["ParameterItem"]

from dataclasses import KW_ONLY
from dataclasses import dataclass
from typing import List

from .constants import PARM_TYPE_CHOICE
from .constants import PARM_TYPE_DEFAULT
from .constants import PARM_TYPE_INDEX
from .constants import UNDEFINED_VALUE
from .constants import _PARM_WIDGET_KEYS


@dataclass()
class ParameterItem:
    """Each parameter to be edited has several pieces of information:"""

    label: str
    value: (int, str)
    _: KW_ONLY  # all parameters below are specified by keyword
    default_value: (int, str) = UNDEFINED_VALUE
    widget: str = PARM_TYPE_DEFAULT
    tooltip: str = ""
    choices: List[str] = UNDEFINED_VALUE
    hi: int = UNDEFINED_VALUE
    lo: int = UNDEFINED_VALUE

    def __post_init__(self):
        """Validate the inputs."""
        # print(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}()")

        if self.widget == PARM_TYPE_CHOICE:
            if self.choices == UNDEFINED_VALUE:
                raise ValueError(
                    'Must be list of choices: \'choices=["one", "two", ...]\''
                )

        elif self.widget == PARM_TYPE_INDEX:
            # print(f"{self.choices=!r}")
            if self.hi == UNDEFINED_VALUE:
                raise ValueError("Must provide hi (maximum value), example: 'hi=9'")
            if self.lo == UNDEFINED_VALUE:
                raise ValueError("Must provide lo (minimum value), example: 'lo=0'")
            if self.lo > self.hi:
                raise ValueError(
                    f"Received 'lo={self.lo}' which is greater than 'hi={self.hi}'."
                )
            # fmt: off
            if int(self.value) > self.hi:
                raise ValueError(
                    f"Received 'value={self.value}."
                    f"  Cannot be greater than: hi={self.hi}'."
                )
            if int(self.value) < self.lo:
                raise ValueError(
                    f"Received 'value={self.value}."
                    f"  Cannot be less than: lo={self.lo}'."
                )
            # fmt: on

        elif self.widget not in _PARM_WIDGET_KEYS:
            raise ValueError(
                f"Received 'widget={self.widget!r}.  Must be one of {_PARM_WIDGET_KEYS}."
            )


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2024, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
