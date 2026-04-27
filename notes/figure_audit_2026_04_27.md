# Figure Audit — NeurIPS 2026 paper
*Date: 2026-04-27*
*Auditor: spotlight-grade layout pass on 13 paper figures*

Bar: "would Nature Neuroscience accept this layout?"

## Methodology
1. Each PNG rendered at 400 dpi was inspected for: overlaps, cramped panels, truncated text,
   mismatched panels, inconsistent fonts, colorbar/axis interference, panel-label collisions,
   and tight-layout artefacts.
2. For each issue identified the script in `figures/{landmark,neuro}/scripts/` was edited
   and re-run with `/home/radwany/miniconda3/envs/hfnewest/bin/python3` from `EEG_Emotion/`.
3. The regenerated PNG was re-read and the iteration repeated until clean.

## Note on output paths
The scripts originally wrote ONLY to `/ibex/project/c2323/yousef/paper_neurips26_final/figures/{landmark,neuro}`,
but the paper builds from `figures/{landmark,neuro}` under `EEG_Emotion/`. Each modified
script now writes to BOTH locations so both trees stay in sync.

---
