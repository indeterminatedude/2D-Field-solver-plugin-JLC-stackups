"""Action plugin. Run() only opens the calculator in the browser.

KiCad 10 on macOS loads this from:
  ~/Documents/KiCad/10.0/scripting/plugins/field_solver/__init__.py
Do not put plugin.json in this folder.
"""

import os
import webbrowser

import pcbnew

HTML_NAME = "field_solver.html"


def _html_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), HTML_NAME)


def _selected_track_width_mm():
    board = pcbnew.GetBoard()
    if board is None:
        return None
    try:
        via_type = pcbnew.PCB_VIA
    except Exception:
        via_type = ()
    for item in board.GetTracks():
        if not item.IsSelected():
            continue
        if via_type and isinstance(item, via_type):
            continue
        return pcbnew.ToMM(item.GetWidth())
    return None


class FieldSolverPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "2D Field Solver"
        self.category = "RF Tools"
        self.description = "Transmission-line impedance with JLCPCB stackups"
        self.show_toolbar_button = False

    def Run(self):
        path = _html_path()
        url = "file://" + path
        width = None
        try:
            width = _selected_track_width_mm()
        except Exception:
            width = None
        if width is not None:
            url += "?w={:.4f}".format(width)
        webbrowser.open(url)


FieldSolverPlugin().register()
