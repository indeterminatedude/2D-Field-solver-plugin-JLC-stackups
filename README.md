# 2D Field Solver

Impedance calculator for PCB transmission lines. Pick a structure, type the geometry (or load a JLCPCB stackup), and read Z₀, εeff, wavelength, and delay. The cross-section sits on the right; the inputs stay on the left.

Built for board work where you want a number before you open the fab's impedance table.

## Structures

| Structure | What you get |
| --- | --- |
| Microstrip | Z₀, εeff. Hammerstad–Jensen, with a thickness correction on W. |
| Embedded microstrip | Same, with a cover height H2 pulling εeff toward εr. |
| Edge-coupled microstrip | Zodd, Zeven, and Zdiff ≈ 2·Zodd. |
| Stripline | Symmetric IPC-2141 style Z₀. εeff is the bulk εr. Plane spacing is B. |
| Coplanar waveguide | Conductor-backed CPW. Gap S is the slot to the coplanar ground. |

Ground checkboxes mark which conductors are the return: bottom plane, top plane, and coplanar side grounds.

## Using it

Open the app and work down the left column.

- **Structure** changes the cross-section and which inputs matter (S, H2, B).
- **JLCPCB stackup** fills εr, dielectric height, and finished copper for a published JLC build. Outer layers load as microstrip. Inner layers load as stripline. These are nominal post-lamination numbers, not a controlled-impedance quote.
- **Units** are mm or mil. The solver converts to mm internally.
- **Calculate** runs the closed-form model. **Solve Fields** draws a quasi-static potential (SOR on ∇·(ε∇φ) = 0) over the cross-section. The impedance number on screen is the analytical one. Treat the field plot as a picture of where the energy sits, not as a second Z₀.

Frequency only affects wavelength and delay (ps/mm). It does not add dispersion.

### JLCPCB presets

| Preset | Use |
| --- | --- |
| 2-layer 1.6 mm, 1 oz | Outer microstrip, H ≈ 1.5 mm, εr ≈ 4.5 |
| JLC04161H-7628 outer / inner | H = 0.210 mm, εr 4.4 / stripline B ≈ 1.065 mm, εr 4.6 |
| JLC04161H-3313 outer / inner | H = 0.099 mm, εr 4.1 / stripline B ≈ 1.265 mm, εr 4.6 |
| JLC04161H-1080 outer / inner | H = 0.076 mm, εr 3.91 / stripline B ≈ 1.265 mm, εr 4.6 |
| 6-layer 1.6 mm, typical outer | H ≈ 0.1 mm, εr ≈ 4.1 |

Finished copper in the presets is 1 oz outer and 0.5 oz inner. Check the current JLC stackup drawing before you lock a design. Prepreg thickness moves.

## KiCad

The same page is an action plugin. From the header, **Download KiCad plugin**, then unzip so the folder is named `field_solver` and contains `__init__.py` and `field_solver.html`.

| OS | Plugins folder |
| --- | --- |
| Linux | `~/.local/share/kicad/9.0/scripting/plugins/` |
| macOS | `~/Library/Preferences/kicad/9.0/scripting/plugins/` |
| Windows | `%APPDATA%\kicad\9.0\scripting\plugins\` |

Use `8.0` in that path if that is the KiCad you run. Then in the PCB editor: **Tools → External Plugins → Refresh Plugins**, and open **2D Field Solver**.

If a track is selected, its width is loaded as W. Vias are ignored. The dialog uses wxHTML if KiCad's Python has it, otherwise it opens the page in a browser.

Source for the plugin is [`kicad-plugin/field_solver`](kicad-plugin/field_solver). The single-file calculator is [`public/solver.html`](public/solver.html). It also runs on its own: open that file in a browser, no server required.

The page exposes `FieldSolver.getResult()`, `FieldSolver.getInputs()`, and `FieldSolver.setInputs({...})` if you want to drive it from another script. Launch query keys: `w`, `h`, `t`, `s`, `er`, `b`, `freq`, `structure`.

## Limits

These are quasi-TEM formulas for a first cut. They do not include soldermask, etchback, roughness, or frequency dispersion. Edge-coupled and embedded models are approximations on top of the microstrip formula. For a controlled-impedance fab note, use the stackup JLCPCB (or your fab) publishes for that exact order, and keep this tool for the sweep before you send it.
