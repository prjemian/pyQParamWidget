"""
Parameter Editor: dialog for user-editable application parameters.

.. autosummary::

   ~ParameterEditorWidget
   ~ParameterItem
"""

from dataclasses import KW_ONLY
from dataclasses import dataclass
from typing import List

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from .constants import PARM_TYPE_CHECKBOX
from .constants import PARM_TYPE_CHOICE
from .constants import PARM_TYPE_DEFAULT
from .constants import PARM_TYPE_INDEX
from .constants import UNDEFINED_VALUE


_PARM_WIDGETS = {
    PARM_TYPE_CHECKBOX: QtWidgets.QCheckBox,
    PARM_TYPE_CHOICE: QtWidgets.QComboBox,
    PARM_TYPE_DEFAULT: QtWidgets.QLineEdit,
    PARM_TYPE_INDEX: QtWidgets.QSpinBox,
}
_PARM_WIDGET_KEYS = list(_PARM_WIDGETS.keys())


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


class ParameterEditorWidget(QtWidgets.QWidget):
    """
    Edit parameters of one section.

    Caller should not close this window if 'self.dirty()'
    returns 'True'.

    PARAMETERS

    - parent (object): QWidget parent
    - parameters (dict): Dictionary of ParameterItem objects, keys are defined
      by the caller.

    ..  autosummary::

        ~currentValues
        ~do_cancel
        ~do_ok
        ~dirty
        ~setDirty
    """

    ui_file = "param_editor.ui"

    def __init__(self, parent, parameters={}):
        from .utils import myLoadUi

        self.parent = parent
        self.parameters = parameters

        super().__init__(parent)
        myLoadUi(self.ui_file, baseinstance=self)
        self.setup()
        self.setDirty(False)  # unsaved changes if True

    def setup(self):
        self.editors = {}
        for k, pitem in self.parameters.items():
            editor = _PARM_WIDGETS[pitem.widget](self)

            def checkIfDirty(_v):  # _v (new value) ignored here
                """If dirty, then widget value(s) are not as provided."""
                dirty = len(self.changedValues()) > 0
                self.setDirty(dirty)

            if pitem.tooltip != "":
                editor.setToolTip(pitem.tooltip)

            if pitem.widget == PARM_TYPE_CHECKBOX:
                editor.setTristate(on=False)
                editor.setCheckState(2 if pitem.value else 0)
                editor.stateChanged.connect(checkIfDirty)
            elif pitem.widget == PARM_TYPE_CHOICE:
                editor.addItems(pitem.choices)
                editor.setCurrentText(str(pitem.value))
                editor.currentTextChanged.connect(checkIfDirty)
            elif pitem.widget == PARM_TYPE_INDEX:
                editor.setRange(pitem.lo, pitem.hi)
                editor.setValue(pitem.value)
                editor.valueChanged.connect(checkIfDirty)
            else:
                editor.setText(str(pitem.value))
                editor.textChanged.connect(checkIfDirty)

            label = QtWidgets.QLabel(self, text=pitem.label)
            self.form_layout.addRow(label, editor)
            self.editors[k] = editor

        self.do_cancel()  # sets editor widgets to supplied values
        self.btn_cancel.clicked.connect(self.do_cancel)
        self.btn_ok.clicked.connect(self.do_ok)

    def changedValues(self):
        """Return dictionary with any changed values."""
        results = {}
        for k, editor in self.editors.items():
            pitem = self.parameters[k]
            original_type = type(pitem.value)
            if pitem.widget == PARM_TYPE_CHECKBOX:
                get_widget_value = editor.checkState
            elif pitem.widget == PARM_TYPE_CHOICE:
                get_widget_value = editor.currentText
            elif pitem.widget == PARM_TYPE_INDEX:
                get_widget_value = editor.value
            else:
                get_widget_value = editor.text
            # Report result using original data type.
            v = original_type(get_widget_value())
            if v != pitem.value:
                results[k] = v
        return results

    @QtCore.pyqtSlot()
    def do_cancel(self):
        """Set all widgets to original values. Set dirty flag to False."""
        # print(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}()")
        for k, editor in self.editors.items():
            pitem = self.parameters[k]
            if pitem.widget == PARM_TYPE_CHECKBOX:
                editor.setCheckState(2 if pitem.value else 0)
            elif pitem.widget == PARM_TYPE_CHOICE:
                editor.setCurrentText(str(pitem.value))
            elif pitem.widget == PARM_TYPE_INDEX:
                editor.setValue(pitem.value)
            else:
                editor.setText(str(pitem.value))
        self.setDirty(False)

    @QtCore.pyqtSlot()
    def do_ok(self):
        """
        Return dict with current values of all widgets.
        """
        # print(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}()")
        for k, v in self.changedValues().items():
            parm = self.parameters[k]
            parm.value = v  # update
        self.setDirty(False)

    def dirty(self) -> bool:
        """Have values been changed?"""
        return self._dirty

    def setDirty(self, dirty: bool):
        """
        Set the dirty (values have changed) flag.  Make it visible.
        """
        self._dirty = dirty
        self.btn_ok.setEnabled(dirty)
        self.btn_cancel.setEnabled(dirty)


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2024, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
