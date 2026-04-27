"""Landmark-grade publication style — matches the topography agent's style.

All landmark figures share these rcParams + a common color palette so the
paper has a consistent visual identity (Helvetica, no top/right spines,
RdBu_r for signed r, viridis for unsigned magnitudes).
"""
import matplotlib as mpl


COLORS = {
    "blue":      "#1f77b4",
    "red":       "#d62728",
    "gray":      "#7f7f7f",
    "darkblue":  "#0d4373",
    "lightblue": "#9ecae1",
    "orange":    "#ff7f0e",
    "green":     "#2ca02c",
    "lightgray": "#d9d9d9",
    "purple":    "#9467bd",
    "lightred":  "#fcd1d1",

    # phase colors (cascade)
    "prior":     "#bdbdbd",
    "replication": "#9ecae1",
    "recipe":    "#3a8dde",
    "ensemble":  "#0d4373",
    "sota":      "#08306b",

    # tier colors (interventions forest plot)
    "destruction": "#5a0e0e",
    "monotonic":   "#7f1c1c",
    "neg_sig":     "#d62728",
    "neg_ns":      "#ff9933",
    "ns":          "#bdbdbd",
    "pos_ns":      "#9ecae1",
    "pos_sig":     "#2ca02c",

    # 9-emotion FACED valence palette (negative→positive)
    "Anger":       "#7a0e0e",
    "Disgust":     "#c0392b",
    "Fear":        "#e67e22",
    "Sadness":     "#a07b3a",
    "Neutral":     "#7f7f7f",
    "Amusement":   "#74b266",
    "Inspiration": "#3a8dde",
    "Joy":         "#1f77b4",
    "Tenderness":  "#0d4373",
}


def apply_lf_style():
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 9,
        "axes.labelsize": 9,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "figure.titlesize": 12,
        "figure.dpi": 150,
        "savefig.dpi": 400,
        "savefig.bbox": "tight",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.9,
        "xtick.major.width": 0.9,
        "ytick.major.width": 0.9,
        "xtick.major.size": 3.0,
        "ytick.major.size": 3.0,
        "lines.linewidth": 1.5,
        "axes.grid": False,
        "axes.unicode_minus": True,
        "mathtext.fontset": "dejavusans",
        "figure.constrained_layout.use": False,  # most LFs use manual gridspec
    })


def save_dual(fig, base_path):
    """Save fig as PDF (vector) + PNG (400 dpi raster)."""
    fig.savefig(f"{base_path}.pdf", bbox_inches="tight")
    fig.savefig(f"{base_path}.png", dpi=400, bbox_inches="tight")
    print(f"  saved -> {base_path}.pdf / .png")


def panel_label(ax, label, x=-0.13, y=1.05, fontsize=12):
    """Place a bold panel label (a, b, c, ...) at the top-left of an axis."""
    ax.text(x, y, label, transform=ax.transAxes,
            fontsize=fontsize, fontweight="bold",
            va="bottom", ha="left")
