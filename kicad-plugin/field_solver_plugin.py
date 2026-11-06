"""Drop this file directly into KiCad's scripting/plugins folder.

macOS KiCad 10:
  ~/Documents/KiCad/10.0/scripting/plugins/field_solver_plugin.py

field_solver.html must sit next to this file, or in ./field_solver/.
Quit KiCad completely after copying. Refresh Plugins does not reload a
plugin that already failed to import.
"""

import os
import webbrowser

import pcbnew


def _html_path():
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "field_solver.html"),
        os.path.join(here, "field_solver", "field_solver.html"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    return candidates[0]


class FieldSolverPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "2D Field Solver"
        self.category = "RF Tools"
        self.description = "Transmission-line impedance with JLCPCB stackups"
        self.show_toolbar_button = False

    def Run(self):
        path = _html_path()
        webbrowser.open("file://" + path)


FieldSolverPlugin().register()
