"""
Parameter Editor: dialog for user-editable application parameters.

.. autosummary::

   ~ParameterEditorWidget
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from .constants import PARM_TYPE_CHECKBOX
from .constants import PARM_TYPE_CHOICE
from .constants import PARM_TYPE_INDEX
from .constants import _PARM_WIDGETS


class ParameterEditorWidget(QtWidgets.QWidget):
    """
    Edit a set of parameters in a scrollable QWidget.

    * Caller should not close this window if
      ``ParameterEditorWidget.dirty()``
      returns 'True'.

    * Caller should call ``ParameterEditorWidget.changedValues()``
      for a dictionary of any changed values.  Dictionary keys
      are *as-supplied* by user in ``parameters``.

    PARAMETERS

    - parent (object): QWidget parent
    - parameters (dict): Dictionary of ParameterItem objects,
      keys are defined by the caller.

    ..  autosummary::

        ~changedValues
        ~dirty
        ~do_accept
        ~do_reset
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

        self.do_reset()  # sets editor widgets to supplied values
        self.btn_reset.clicked.connect(self.do_reset)
        self.btn_accept.clicked.connect(self.do_accept)

    def changedValues(self):
        """Return dictionary with only the changed values."""
        changes = {}
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
                changes[k] = v
        return changes

    @QtCore.pyqtSlot()
    def do_reset(self):
        """Update widget values from original values and clear dirty flag."""
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
    def do_accept(self):
        """
        Update original values from widget values and clear dirty flag.
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
        self.btn_accept.setEnabled(dirty)
        self.btn_reset.setEnabled(dirty)


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2024, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
