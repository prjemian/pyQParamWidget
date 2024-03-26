"""Parameters Editor Demo"""
import sys

from PyQt5 import QtWidgets


PARMS_FILE = "sampler.yml"
PARMS_FILE = "example.yml"


def read_parameter_specifications(parms_file):
    """Read application parameter specifications from YAML file."""
    import yaml
    import pyqparamwidget as qpw

    with open(parms_file) as f:
        specs = yaml.load(f.read(), Loader=yaml.Loader)
    parms = {}
    for k, v in specs["parameters"].items():
        args = [v["label"], v["value"]]
        kwargs = {
            kw: v[kw]
            for kw in "widget choices hi lo tooltip".split()
            if v.get(kw) is not None
        }
        parms[k] = qpw.ParameterItem(*args, **kwargs)
    return parms


def main():
    from pyqparamwidget import ParameterEditorWidget

    parms = read_parameter_specifications(PARMS_FILE)
    app = QtWidgets.QApplication(sys.argv)
    window = ParameterEditorWidget(None, parms)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
