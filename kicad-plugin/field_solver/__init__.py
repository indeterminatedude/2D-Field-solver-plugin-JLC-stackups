"""KiCad action plugin: 2D transmission-line field solver.

Install: copy this folder into KiCad's scripting plugins directory, then
Tools -> External Plugins -> Refresh Plugins.

  KiCad 10 (macOS): ~/Documents/KiCad/10.0/scripting/plugins/field_solver
  KiCad 9:  ~/Documents/KiCad/9.0/scripting/plugins/field_solver
  KiCad 8:   ~/.local/share/kicad/8.0/scripting/plugins/field_solver   (Linux)
             ~/Library/Preferences/kicad/8.0/scripting/plugins/field_solver
             %APPDATA%\\kicad\\8.0\\scripting\\plugins\\field_solver

If a track is selected, its width is passed in as W (mm).
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
    for item in board.GetTracks():
        if not item.IsSelected():
            continue
        if isinstance(item, pcbnew.PCB_VIA):
            continue
        return pcbnew.ToMM(item.GetWidth())
    return None


def _file_url():
    path = _html_path().replace("\\", "/")
    if os.name == "nt" and not path.startswith("/"):
        path = "/" + path
    url = "file://" + path
    width = _selected_track_width_mm()
    if width is not None:
        url += "?w={:.4f}".format(width)
    return url


class FieldSolverPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "2D Field Solver"
        self.category = "RF Tools"
        self.description = (
            "Microstrip, embedded microstrip, edge-coupled, stripline, and CPW "
            "impedance with JLCPCB stackups."
        )
        self.show_toolbar_button = True

    def Run(self):
        url = _file_url()
        try:
            self._show_dialog(url)
        except Exception:
            webbrowser.open(url)

    def _show_dialog(self, url):
        import wx
        import wx.html2

        # KiCad 10's wx app is an AppConsole and has no GetTopWindow.
        parent = None
        getter = getattr(wx, "GetTopLevelWindows", None)
        if getter:
            windows = getter()
            if windows:
                parent = windows[0]

        dialog = wx.Dialog(
            parent,
            title="2D Field Solver",
            size=(1280, 800),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX,
        )
        web = wx.html2.WebView.New(dialog)
        web.LoadURL(url)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(web, 1, wx.EXPAND)
        dialog.SetSizer(sizer)
        dialog.Centre()
        dialog.ShowModal()
        dialog.Destroy()


FieldSolverPlugin().register()
