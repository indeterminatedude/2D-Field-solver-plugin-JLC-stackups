"""KiCad 10 action plugin. Copy this file into:

  ~/Documents/KiCad/10.0/scripting/plugins/field_solver_plugin.py

field_solver.html must sit in that same folder. Quit KiCad after copying.
The toolbar icon is written next to this file on first load.
"""

import base64
import os

import pcbnew

_frame = None

_ICON_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAABV0lEQVR4nO2asa4BQRSGzw4v"
    "oFFR0KC+DVqvIBJPoFVL7m003kRy30GLRyARCiqNJxCqTcaaM8fusGeOzNftzqz5/jl7NrIA"
    "CCeiJlRqzVseIhinw8bqiA5yiyfBgijTSd/kAXCnpwA+yseY3BQ1wTeSjgob8Bnd1dgDkogA"
    "3HZ/uVo7S3Q77UzXnQ6bSHwFiq4fQO1eXKGsu0wRKkDxqZ2PIQMsBnt0rPdffzje/h5fXrgx"
    "rWZeR+dtt1Aa+SzzMcT3QAjAjbWJS8MywBVvrtKwrB2lv6cfrifWuczPxrG3VaC9+/nofAzy"
    "MdovvP4cd5FKs46O+B4IAbgJAbgJAbgJAbgJAbgRH8D6ZW7UmuTlQTKDsfG8+AqEANxYA8z+"
    "xjlp2LF5OL+d5uQr3k4rAPqnTB+Jnb+jAgCyqqC7KmzAV5KOT7eQzyFMbsYe8DEE5iT+zx7i"
    "uQPPwmFezxDnvAAAAABJRU5ErkJggg=="
)


def _here():
    return os.path.dirname(os.path.abspath(__file__))


def _html_path():
    here = _here()
    for path in (
        os.path.join(here, "field_solver.html"),
        os.path.join(here, "field_solver", "field_solver.html"),
    ):
        if os.path.isfile(path):
            return path
    return os.path.join(here, "field_solver.html")


def _icon_path():
    path = os.path.join(_here(), "icon.png")
    if not os.path.isfile(path):
        try:
            with open(path, "wb") as handle:
                handle.write(base64.b64decode(_ICON_B64))
        except Exception:
            return ""
    return path


def _selected_width_mm():
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
        self.show_toolbar_button = True
        icon = _icon_path()
        if icon:
            self.icon_file_name = icon
            self.dark_icon_file_name = icon

    def Run(self):
        global _frame
        import wx
        import wx.html2

        if _frame is not None:
            try:
                if _frame.IsShown():
                    _frame.Raise()
                    return
            except RuntimeError:
                _frame = None

        # KiCad 10's app object has no GetTopWindow, so the frame is parentless.
        frame = wx.Frame(None, title="2D Field Solver", size=(1180, 760))
        web = wx.html2.WebView.New(frame)
        path = _html_path()
        with open(path, "r", encoding="utf-8") as handle:
            html = handle.read()
        width = None
        try:
            width = _selected_width_mm()
        except Exception:
            width = None
        if width is not None:
            def _fill(_event, view=web, millimetres=width):
                view.RunScript(
                    "if (window.FieldSolver) FieldSolver.setInputs({w: %.4f});" % millimetres
                )
            web.Bind(wx.html2.EVT_WEBVIEW_LOADED, _fill)
        web.SetPage(html, "file://" + os.path.dirname(path).replace("\\", "/") + "/")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(web, 1, wx.EXPAND)
        frame.SetSizer(sizer)
        icon = _icon_path()
        if icon:
            try:
                frame.SetIcon(wx.Icon(icon, wx.BITMAP_TYPE_PNG))
            except Exception:
                pass
        frame.Centre()
        frame.Show()
        _frame = frame


FieldSolverPlugin().register()
