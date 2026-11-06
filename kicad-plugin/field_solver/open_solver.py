"""KiCad 10 IPC entry. Opens the calculator and passes a selected track width."""

import os
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "field_solver.html")


def _selected_width_mm():
    try:
        from kipy import KiCad
        from kipy.board_types import Track
    except Exception:
        return None
    try:
        board = KiCad().get_board()
        for item in board.get_selection():
            if not isinstance(item, Track):
                continue
            width = getattr(item, "width", None)
            if not isinstance(width, (int, float)) or width <= 0:
                continue
            # IPC lengths are nanometres.
            return width / 1e6 if width > 100 else float(width)
    except Exception:
        return None
    return None


def main():
    path = HTML.replace("\\", "/")
    if os.name == "nt" and not path.startswith("/"):
        path = "/" + path
    url = "file://" + path
    width = _selected_width_mm()
    if width is not None:
        url += "?w={:.4f}".format(width)
    webbrowser.open(url)


if __name__ == "__main__":
    main()
