"""Common matplotlib style for NeurIPS 2026 paper figures.

Usage:
    from _style import apply_style, COLORS
    apply_style()
"""
import matplotlib as mpl
import matplotlib.pyplot as plt


COLORS = {
    "blue": "#1f77b4",      # positive
    "red": "#d62728",       # negative
    "gray": "#7f7f7f",      # neutral / null
    "darkblue": "#0d4373",  # ensemble / strong positive
    "lightblue": "#9ecae1",
    "orange": "#ff7f0e",
    "green": "#2ca02c",
    "lightgray": "#d9d9d9",
    "purple": "#9467bd",
    "cbra": "#1f77b4",      # CBraMod
    "emod": "#d62728",      # EMOD
}


def apply_style():
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica"],
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "figure.titlesize": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "lines.linewidth": 1.5,
        "axes.grid": False,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "pdf.fonttype": 42,  # editable text
        "ps.fonttype": 42,
        "axes.unicode_minus": True,
    })


def save_dual(fig, base_path):
    """Save fig as PDF (vector) + PNG preview at the same base path."""
    fig.savefig(f"{base_path}.pdf", dpi=300, bbox_inches="tight")
    fig.savefig(f"{base_path}.png", dpi=180, bbox_inches="tight")
