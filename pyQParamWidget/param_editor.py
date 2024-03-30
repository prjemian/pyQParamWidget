"""
Parameter Editor: dialog for user-editable application parameters.

This Python code defines a PyQt5 widget called
``ParameterEditor``. It is used for editing a set of parameters
and provides functionality for accepting or resetting changes
made to the parameter values.

.. autosummary::

   ~ParameterEditor
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from .utils import unsaved_changes_alert_dialog


class ParameterEditor(QtWidgets.QWidget):
    """
    Edit a set of parameters in a scrollable QWidget.

    Here is a breakdown of the key components and their purpose:

    * The class inherits from ``QtWidgets.QWidget`` and
      represents a scrollable widget for editing a set of
      parameters.

    * The ``ui_file`` attribute specifies the path to the UI
      file used for building the GUI. The ``myLoadUi`` function
      is used to load the UI file and populate the widget with
      the necessary elements.

    Overall, this code provides a flexible parameter editing
    widget with the ability to track changes, validate inputs,
    and handle user interactions for accepting or resetting
    changes.

    NOTES FOR THE CALLER

    * Caller should not close this window if
      ``ParameterEditor.dirty()`` returns ``True``.

    * Before closing this window:

      * User must ``Accept`` or ``Reset`` any changes (which sets ``dirty=False``).
      * Verify: ``ParameterEditor.dirty() == True``
      * Get values: ``results = ParameterEditor.values()``

    ATRRIBUTES

    - ui_file (str): Names the UI file used for building the GUI.
      The ``myLoadUi`` function is used to load the UI file and
      populate the widget with the necessary elements.

    PARAMETERS

    - parent (object): QWidget parent

    - parameters (dict): Dictionary of ParameterItemBase objects.
      These objects represent the parameters that will be
      displayed and edited in the ``ParameterEditor`` widget.
      Each parameter is associated with a key defined by the
      caller.

    ..  autosummary::

        ~changedValues
        ~dirty
        ~do_accept
        ~do_reset
        ~setDirty
        ~values
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
        """
        Build the QFormLayout with the parameters.

        The ``setup`` method builds the GUI layout by creating
        editor widgets for each parameter and adding them to a
        ``QFormLayout`` along with their associated labels.
        """
        self.editors = {}

        def checkIfDirty(_v):  # _v (new value) ignored here
            """If dirty, then widget value(s) are not as provided."""
            dirty = len(self.changedValues()) > 0
            self.setDirty(dirty)

        def add_parameter_widget(pitem):
            editor = pitem.widget_class(self, parameter=pitem)
            editor.qpw_setup(pitem, checkIfDirty)

            label = QtWidgets.QLabel(self, text=pitem.label)
            self.form_layout.addRow(label, editor)
            return editor

        # Remember each parameter's editor widget.
        self.editors = {
            k: add_parameter_widget(pitem) for k, pitem in self.parameters.items()
        }

        self.do_reset()  # sets editor widgets to supplied values
        self.btn_reset.clicked.connect(self.do_reset)
        self.btn_accept.clicked.connect(self.do_accept)

    def changedValues(self):
        """
        Return dictionary with only the changed values.

        The ``changedValues`` method returns a dictionary
        containing only the parameter values that have been
        changed by the user.

        .. note:: Result is always empty dictionary when
           ``dirty==True``.  Use :meth:`~pyQParamWidget.param_editor.ParameterEditor.values()` to get the final values.
        """
        return {
            k: editor.qpw_get()
            for k, editor in self.editors.items()
            if editor.qpw_isChanged()
        }

    def closeEvent(self, event):
        """
        Do not allow editor to be closed if there are unresolved changes.

        The ``closeEvent`` method is overridden to prevent the
        widget from being closed if there are any unsaved changes.
        It displays an alert dialog to inform the user about the
        unsaved changes.
        """
        if self.dirty():
            unsaved_changes_alert_dialog(self)
            event.ignore()
        else:
            event.accept()

    @QtCore.pyqtSlot()
    def do_accept(self):
        """
        Update original values from widget values and clear dirty flag.

        Called when the *Accept* button is pressed.
        """
        # print(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}()")
        for k, v in self.changedValues().items():
            parm = self.parameters[k]
            parm.value = v  # update
        self.setDirty(False)

    @QtCore.pyqtSlot()
    def do_reset(self):
        """
        Update widget values from original values and clear dirty flag.

        Called when the *Reset* button is pressed.
        """
        # print(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}()")
        for k, editor in self.editors.items():
            editor.qpw_set(self.parameters[k].value)
        self.setDirty(False)

    def dirty(self) -> bool:
        """
        Have values been changed?

        The ``dirty`` method returns a boolean indicating whether
        there are any unsaved changes in the widget.
        """
        return self._dirty

    def setDirty(self, dirty: bool):
        """
        Set the dirty (values have changed) flag.  Make it visible.

        The ``setDirty`` method sets the dirty flag and
        enables or disables the Accept and Reset buttons
        accordingly.
        """
        self._dirty = dirty
        self.btn_accept.setEnabled(dirty)
        self.btn_reset.setEnabled(dirty)

    def values(self):
        """
        Returns a dictionary containing the current widget values of all parameters.
        """
        return {k: editor.qpw_get() for k, editor in self.editors.items()}


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2024, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
