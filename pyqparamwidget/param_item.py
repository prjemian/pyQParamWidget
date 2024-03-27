"""
Parameter Item

.. autosummary::
   ~ParameterItemBase
   ~ParameterItemCheckbox
   ~ParameterItemChoice
   ~ParameterItemIndex
   ~ParameterItemText
"""

# TODO: refactor (throughout the package) to use subclasses

__all__ = ["ParameterItemBase"]

from dataclasses import KW_ONLY
from dataclasses import dataclass
from typing import List

from .qpw_widgets import PARM_TYPE_CHECKBOX
from .qpw_widgets import PARM_TYPE_CHOICE
from .qpw_widgets import PARM_TYPE_DEFAULT
from .qpw_widgets import PARM_TYPE_INDEX
from .qpw_widgets import UNDEFINED_VALUE
from .qpw_widgets import _PARM_WIDGET_KEYS
from .qpw_widgets import QPW_CheckBox
from .qpw_widgets import QPW_Choice
from .qpw_widgets import QPW_Index
from .qpw_widgets import QPW_Text


@dataclass()
class ParameterItemBase:
    """Each parameter to be edited has several pieces of information."""

    label: str
    """Form text for this item."""

    value: (int, str)
    """Supplied (or accepted) value."""

    _: KW_ONLY  # all parameters below are specified by keyword

    widget: str = PARM_TYPE_DEFAULT  # TODO: needed?
    """Widget type for this item."""

    tooltip: str = ""
    """Widget tooltip for this item."""

    choices: List[str] = UNDEFINED_VALUE
    """List of choices if widget=PARM_TYPE_CHOICE."""

    hi: int = UNDEFINED_VALUE
    """Maximum value for widget=PARM_TYPE_INDEX."""

    lo: int = UNDEFINED_VALUE
    """Minimum value for widget=PARM_TYPE_INDEX."""

    def validate(self):
        raise NotImplementedError("Implement in the subclass.")

    def __post_init__(self):
        """Validate the inputs."""
        # print(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}()")

        if self.widget in _PARM_WIDGET_KEYS:
            self.validate()  # TODO: verify this
        else:
            raise ValueError(
                f"Received 'widget={self.widget!r}.  Must be one of {_PARM_WIDGET_KEYS}."
            )


class ParameterItemCheckbox(ParameterItemBase):
    """Edit a checkbox parameter."""

    widget = PARM_TYPE_CHECKBOX

    def __init__(self, label, value, tooltip=""):
        super().__init__(label, value, tooltip=tooltip, widget=self.widget)

    def validate(self):
        """Validation not necessary for checkbox."""
        pass


class ParameterItemChoice(ParameterItemBase):
    """Choose a parameter value from a list."""

    widget = PARM_TYPE_CHOICE
    widget_class = QPW_Choice

    def __init__(self, label, value, choices=[], tooltip=""):
        super().__init__(
            label, value, tooltip=tooltip, choices=choices, widget=self.widget
        )

    def validate(self):
        """Must provide a list of choices."""
        if self.choices == UNDEFINED_VALUE:
            raise ValueError('Must be list of choices: \'choices=["one", "two", ...]\'')


class ParameterItemIndex(ParameterItemBase):
    """Set a numerical parameter between lo & hi."""

    widget = PARM_TYPE_INDEX
    widget_class = QPW_Index

    def __init__(
        self, label, value, hi=UNDEFINED_VALUE, lo=UNDEFINED_VALUE, tooltip=""
    ):
        super().__init__(
            label, value, tooltip=tooltip, hi=hi, lo=lo, widget=self.widget
        )

    def validate(self):
        """Must provide lo <= value <= hi."""
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


class ParameterItemText(ParameterItemBase):
    """Edit a text parameter."""

    widget = PARM_TYPE_DEFAULT
    widget_class = QPW_Text

    def __init__(self, label, value, tooltip=""):
        super().__init__(label, value, tooltip=tooltip, widget=self.widget)

    def validate(self):
        """Validation not necessary for text."""
        pass


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2024, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
