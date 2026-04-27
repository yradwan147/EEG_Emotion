"""Publication-grade matplotlib style for the NeurIPS 2026 neuroscience figures."""
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
    "occ":       "#0d4373",  # occipital
    "par":       "#1f77b4",  # parietal
    "cen":       "#7c7c7c",  # central
    "fro":       "#d62728",  # frontal
    "alpha":     "#1976d2",
    "beta":      "#f57c00",
    "delta":     "#5e35b1",
    "theta":     "#00897b",
    "gamma":     "#c62828",
}

BAND_COLORS = {
    "delta": COLORS["delta"],
    "theta": COLORS["theta"],
    "alpha": COLORS["alpha"],
    "beta":  COLORS["beta"],
    "gamma": COLORS["gamma"],
}


def apply_neuro_style():
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "figure.titlesize": 11.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "lines.linewidth": 1.5,
        "axes.grid": False,
        "savefig.dpi": 400,
        "savefig.bbox": "tight",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.unicode_minus": True,
        "mathtext.fontset": "dejavusans",
    })


def save_dual(fig, base_path):
    """Save fig as PDF (vector) + PNG (400 dpi raster)."""
    fig.savefig(f"{base_path}.pdf", bbox_inches="tight")
    fig.savefig(f"{base_path}.png", dpi=400, bbox_inches="tight")
    print(f"  saved -> {base_path}.pdf / .png")
