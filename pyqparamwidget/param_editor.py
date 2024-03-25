"""
Parameter Editor: dialog for user-editable application parameters.

.. autosummary::

   ~ParameterEditorWidget
   ~ParameterItem
   ~PARM_TYPE_CHECKBOX
   ~PARM_TYPE_CHOICE
   ~PARM_TYPE_DEFAULT
   ~PARM_TYPE_INDEX

.. note:: The ``QPW_`` prefix: pyQParamWidget
   
:see: https://www.pythonguis.com/tutorials/pyqt-dialogs/
"""

import sys
from dataclasses import KW_ONLY
from dataclasses import dataclass
from typing import List

from PyQt5 import QtCore
from PyQt5 import QtWidgets

PARM_TYPE_CHECKBOX = "QPW_checkbox"
"""
Widget type for toggling a checkbox or boolean Parameter. (checked: True)

This will produce a QCheckBox widget in the editor.
"""

PARM_TYPE_CHOICE = "QPW_choice"
"""
Widget type for choosing a Parameter from a list.

This will produce a QComboBox widget in the editor.

PARAMETERS

- choices ([str]): List of possible string values.
"""

PARM_TYPE_INDEX = "QPW_index"
"""
Widget type for editing an integer Parameter within a range.

This will produce a QSpinBox widget in the editor.

PARAMETERS

- hi (int): Maximum value.
- lo (int): Minimum value.
"""

PARM_TYPE_DEFAULT = "QPW_default"
"""
Widget type for editing a Parameter as text.

This will produce a QLineEdit widget in the editor.
"""

_PARM_WIDGETS = {
    PARM_TYPE_CHECKBOX: QtWidgets.QCheckBox,
    PARM_TYPE_CHOICE: QtWidgets.QComboBox,
    PARM_TYPE_INDEX: QtWidgets.QSpinBox,
    PARM_TYPE_DEFAULT: QtWidgets.QLineEdit,
}
_PARM_WIDGET_KEYS = list(_PARM_WIDGETS.keys())

_UNDEFINED_VALUE_ = object  # avoids a comparison with None


@dataclass(frozen=True)
class ParameterItem:
    """Each parameter to be edited has several pieces of information:"""

    label: str
    original_value: (int, str)
    _: KW_ONLY  # all parameters below are specified by keyword
    default_value: (int, str) = _UNDEFINED_VALUE_
    widget: str = PARM_TYPE_DEFAULT
    tooltip: str = ""
    choices: List[str] = _UNDEFINED_VALUE_
    hi: int = _UNDEFINED_VALUE_
    lo: int = _UNDEFINED_VALUE_

    def __post_init__(self):
        """Validate the inputs."""
        # print(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}()")

        if self.widget == PARM_TYPE_CHOICE:
            if self.choices == _UNDEFINED_VALUE_:
                raise ValueError(
                    'Must list of choices: \'choices=["one", "two", ...]\''
                )

        elif self.widget == PARM_TYPE_INDEX:
            # print(f"{self.choices=!r}")
            if self.hi == _UNDEFINED_VALUE_:
                raise ValueError("Must provide hi (maximum value), example: 'hi=9'")
            if self.lo == _UNDEFINED_VALUE_:
                raise ValueError("Must provide lo (minimum value), example: 'lo=0'")
            if self.lo > self.hi:
                raise ValueError(
                    f"Received 'lo={self.lo}' which is greater than 'hi={self.hi}'."
                )
            if int(self.original_value) > self.hi:
                raise ValueError(
                    f"Received 'original_value={self.original_value}."
                    f"  Which is greater than: hi={self.hi}'."
                )
            if int(self.original_value) < self.lo:
                raise ValueError(
                    f"Received 'original_value={self.original_value}."
                    f"  Which is less than: lo={self.lo}'."
                )

        elif self.widget not in _PARM_WIDGET_KEYS:
            raise ValueError(
                f"Received 'widget={self.widget!r}.  Must be one of {_PARM_WIDGET_KEYS}."
            )


class ParameterEditorWidget(QtWidgets.QWidget):
    """
    Edit parameters of one section.

    Caller should not close this window if 'self.dirty=True'.

    PARAMETERS

    - parent (object): QWidget parent
    - parameters (dict): Dictionary of ParameterItem objects, keys are defined
      by the caller.

    ..  autosummary::

        ~currentValues ~do_cancel ~do_ok ~do_revert
    """

    ui_file = "param_editor.ui"

    def __init__(self, parent, parameters={}):
        from .utils import myLoadUi

        self.parent = parent
        self.parameters = parameters
        self.dirty = False  # unsaved changes if True

        super().__init__(parent)
        myLoadUi(self.ui_file, baseinstance=self)
        self.setup()

    def setup(self):
        self.editors = {}
        for k, pitem in self.parameters.items():
            editor = _PARM_WIDGETS[pitem.widget](self)

            if pitem.tooltip != "":
                editor.setToolTip(pitem.tooltip)

            if pitem.widget == PARM_TYPE_CHECKBOX:
                editor.setCheckState(pitem.original_value)
            elif pitem.widget == PARM_TYPE_CHOICE:
                editor.addItems(pitem.choices)
                editor.setCurrentText(str(pitem.original_value))
            elif pitem.widget == PARM_TYPE_INDEX:
                editor.setRange(pitem.lo, pitem.hi)
                editor.setValue(pitem.original_value)
            else:
                editor.setText(str(pitem.original_value))

            label = QtWidgets.QLabel(self, text=pitem.label)
            self.form_layout.addRow(label, editor)
            self.editors[k] = editor

        self.do_revert()  # set editor widget to original_value
        self.btn_cancel.clicked.connect(self.do_cancel)
        self.btn_ok.clicked.connect(self.do_ok)
        self.btn_revert.clicked.connect(self.do_revert)

    def currentValues(self):
        """Return dictionary with the current values."""
        results = {}
        for k, editor in self.editors.items():
            orig_type = type(self.parameters[k].original_value)
            widget = self.parameters[k].widget
            if widget == PARM_TYPE_CHECKBOX:
                get_value_function = editor.checkState
            elif widget == PARM_TYPE_CHOICE:
                get_value_function = editor.currentText
            elif widget == PARM_TYPE_INDEX:
                get_value_function = editor.value
            else:
                get_value_function = editor.text
            # Report result using original data type.
            results[k] = orig_type(get_value_function())
        print(f"{results=}")
        return results

    @QtCore.pyqtSlot()
    def do_cancel(self):
        """
        Return empty dict.  No new values.
        """
        print(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}()")
        self.dirty = False
        results = {}
        print(f"{results=}")
        return results

    @QtCore.pyqtSlot()
    def do_ok(self):
        """
        Return dict with current values of all widgets.
        """
        print(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}()")
        self.dirty = False
        # TODO: Should this redefine parm.original_value?
        return self.currentValues()

    @QtCore.pyqtSlot()
    def do_revert(self):
        """Set all widgets to original values."""
        # print(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}()")
        for k, editor in self.editors.items():
            parm = self.parameters[k]
            if parm.widget == PARM_TYPE_CHECKBOX:
                editor.setCheckState(parm.original_value)
            elif parm.widget == PARM_TYPE_CHOICE:
                editor.setCurrentText(str(parm.original_value))
            elif parm.widget == PARM_TYPE_INDEX:
                editor.setValue(parm.original_value)
            else:
                editor.setText(str(parm.original_value))

        self.dirty = False


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2024, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
