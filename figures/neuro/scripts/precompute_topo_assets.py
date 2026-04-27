"""Precompute auxiliary data assets for the NF1-NF5 brain-topography figures.

Pulls raw FACED DE features (28 vid x 32 ch x 30 s x 5 bands; 123 subjects)
plus the LLM V-axis projection vector (28 floats) and produces:

  /ibex/project/c2323/yousef/reports/topography/nf_assets.npz
    - cohort_r_chband        : (32, 5)   per-channel x per-band cohort r vs V
    - drop_class_table       : dict      {28, '9-stim', '25-no-Anger', '19-no-9'} -> r at PO3/gamma
    - per_emotion_drop_delta : (9,)      change in cohort r when dropping each emotion class
    - po3_gamma_per_stim     : (28,)     per-stim PO3/gamma cohort feature (mean across subjects)
    - v_axis                 : (28,)     V-axis projection per stim
    - per_subject_simpson    : (Nsub,)   per-subject r at top-8 fixed channels
    - per_subject_oracle_abs : (Nsub,)   per-subject best (channel, band) |r|
    - time_resolved_cohort   : (5, 30)   cohort r per band per second  (band, t)
    - time_resolved_best_stim: (5, 30)   best-stim cohort r per band per second
    - time_resolved_per_subj_peak: (5, Nsub) argmax t per band per subject
    - connectivity_matrix    : (8, 8)    pairwise gamma-DE corr for top-8 V-axis channels (PO3 F7 O1 P3 Oz O2 P4 PO4)
    - vaxis_top8             : (8,)      channel labels in connectivity order
"""
import os, sys, glob, json, pickle, numpy as np
from scipy.stats import pearsonr

REPORTS = "/ibex/project/c2323/yousef/reports"
DE_DIR = "/ibex/project/c2323/kilich/datasets/FACED/EEG_Features/DE"
OUT = f"{REPORTS}/topography/nf_assets.npz"

FACED_CH = ['Fp1', 'Fp2', 'Fz', 'F3', 'F4', 'F7', 'F8',
            'FC1', 'FC2', 'FC5', 'FC6',
            'Cz', 'C3', 'C4', 'T7', 'T8',
            'CP1', 'CP2', 'CP5', 'CP6',
            'Pz', 'P3', 'P4', 'P7', 'P8',
            'PO3', 'PO4', 'Oz', 'O1', 'O2',
            'A1', 'A2']
BANDS = ['delta', 'theta', 'alpha', 'beta', 'gamma']
# 28 stim are 9 emotions x ~3 stim each (FACED ordering: each emotion contiguous,
# Anger=stim 0..2, Disgust=3..5, Fear=6..8, Sadness=9..11, Neutral=12..15,
# Amusement=16..18, Inspiration=19..21, Joy=22..24, Tenderness=25..27).
EMOTIONS = ['Anger', 'Disgust', 'Fear', 'Sadness', 'Neutral',
            'Amusement', 'Inspiration', 'Joy', 'Tenderness']
EMO_IDX = {
    'Anger':       list(range(0, 3)),
    'Disgust':     list(range(3, 6)),
    'Fear':        list(range(6, 9)),
    'Sadness':     list(range(9, 12)),
    'Neutral':     list(range(12, 16)),  # 4 neutral stim
    'Amusement':   list(range(16, 19)),
    'Inspiration': list(range(19, 22)),
    'Joy':         list(range(22, 25)),
    'Tenderness':  list(range(25, 28)),
}
TOP8 = ['PO3', 'F7', 'O1', 'P3', 'P4', 'C4', 'C3', 'Pz']  # max-|r| across bands
VNET = ['PO3', 'F7', 'O1', 'P3', 'Oz', 'O2', 'P4', 'PO4']  # 8 V-axis network channels


def load_v_axis():
    with open(f"{REPORTS}/r6_clip_only.json") as f:
        d = json.load(f)
    v = np.array(d['clip_bare_emotion_proj'], dtype=np.float64)
    assert v.shape == (28,)
    return v


def load_subject(path):
    with open(path, 'rb') as f:
        d = pickle.load(f)
    # (28, 32, 30, 5)
    return d.astype(np.float32)


def main():
    print("Loading V-axis...", flush=True)
    v = load_v_axis()
    print(f"  v.shape={v.shape}, range=[{v.min():.3f}, {v.max():.3f}]")

    sub_files = sorted(glob.glob(f"{DE_DIR}/sub*.pkl.pkl"))
    print(f"Found {len(sub_files)} subjects")

    print("Loading all subjects (this may take a minute)...", flush=True)
    all_data = []
    for i, p in enumerate(sub_files):
        all_data.append(load_subject(p))
        if (i+1) % 25 == 0:
            print(f"  loaded {i+1}/{len(sub_files)}", flush=True)
    X = np.stack(all_data, axis=0)  # (Nsub, 28, 32, 30, 5)
    Nsub = X.shape[0]
    print(f"X.shape = {X.shape}")

    # ---------- (1) cohort_r_chband ----------
    # Mean over subjects (axis 0) and over time (axis 3) -> (28, 32, 5)
    cohort_stim = X.mean(axis=(0, 3))  # average over subjects then over 30 s
    print(f"cohort_stim shape: {cohort_stim.shape}")

    cohort_r_chband = np.zeros((32, 5), dtype=np.float32)
    for ch in range(32):
        for bd in range(5):
            r = np.corrcoef(cohort_stim[:, ch, bd], v)[0, 1]
            cohort_r_chband[ch, bd] = r

    print(f"cohort_r_chband range: [{cohort_r_chband.min():.3f}, {cohort_r_chband.max():.3f}]")
    print(f"PO3/gamma: {cohort_r_chband[FACED_CH.index('PO3'), 4]:+.4f}")
    print(f"F7/beta:   {cohort_r_chband[FACED_CH.index('F7'),  3]:+.4f}")
    print(f"O1/gamma:  {cohort_r_chband[FACED_CH.index('O1'),  4]:+.4f}")

    # ---------- (2) drop_class_table : r at PO3/gamma for various subsets ----------
    po3_idx = FACED_CH.index('PO3')
    f7_idx = FACED_CH.index('F7')
    o1_idx = FACED_CH.index('O1')
    po3_gamma_per_stim = cohort_stim[:, po3_idx, 4]   # (28,)
    print(f"po3_gamma_per_stim shape: {po3_gamma_per_stim.shape}")

    def r_subset(stim_idx):
        if len(stim_idx) < 3:
            return np.nan
        v_sub = v[stim_idx]
        e_sub = po3_gamma_per_stim[stim_idx]
        return float(np.corrcoef(v_sub, e_sub)[0, 1])

    drop_class_table = {
        'all_28': r_subset(list(range(28))),
        'anger_amus_tend_9': r_subset(EMO_IDX['Anger'] + EMO_IDX['Amusement'] + EMO_IDX['Tenderness']),
        'no_anger_25': r_subset([i for i in range(28) if i not in EMO_IDX['Anger']]),
        'no_9emot_19': r_subset([i for i in range(28) if i not in
                                  (EMO_IDX['Anger'] + EMO_IDX['Amusement'] + EMO_IDX['Tenderness'])]),
    }
    print("drop_class_table:", drop_class_table)

    # ---------- (3) per_emotion_drop_delta ----------
    base_r = drop_class_table['all_28']
    per_emo_drop = []
    for e in EMOTIONS:
        keep = [i for i in range(28) if i not in EMO_IDX[e]]
        r_drop = r_subset(keep)
        per_emo_drop.append(r_drop - base_r)
    per_emotion_drop_delta = np.array(per_emo_drop, dtype=np.float32)
    print("per_emotion_drop_delta:", dict(zip(EMOTIONS, per_emotion_drop_delta)))

    # ---------- (4) Simpson's paradox per-subject distributions ----------
    # per_subject_simpson_top8: For each subject, compute r over 28 stim of
    # mean-across-top-8-channels-and-gamma vs V-axis  (single index per subject).
    per_subj = X.mean(axis=3)  # (Nsub, 28, 32, 5)
    top8_idx = [FACED_CH.index(c) for c in TOP8]
    per_subj_top8_gamma = per_subj[:, :, top8_idx, 4].mean(axis=2)  # (Nsub, 28)

    per_subject_simpson = np.array([
        np.corrcoef(per_subj_top8_gamma[s], v)[0, 1] for s in range(Nsub)
    ], dtype=np.float32)
    print(f"per-subject simpson: mean={per_subject_simpson.mean():.3f}, "
          f"std={per_subject_simpson.std():.3f}, "
          f"range=[{per_subject_simpson.min():.2f}, {per_subject_simpson.max():.2f}]")

    # cohort r at top-8 gamma
    cohort_top8_gamma = per_subj_top8_gamma.mean(axis=0)  # (28,)
    cohort_r_top8 = np.corrcoef(cohort_top8_gamma, v)[0, 1]
    print(f"cohort r at top-8 gamma fixed: {cohort_r_top8:+.4f}")

    # per_subject_oracle: for each subject, find the (channel,band) with max |r|
    per_subject_oracle_abs = np.zeros(Nsub, dtype=np.float32)
    for s in range(Nsub):
        best = 0.0
        for ch in range(32):
            for bd in range(5):
                r = np.corrcoef(per_subj[s, :, ch, bd], v)[0, 1]
                if abs(r) > best:
                    best = abs(r)
        per_subject_oracle_abs[s] = best
    print(f"per-subject oracle |r| mean: {per_subject_oracle_abs.mean():.3f}")

    # ---------- (5) Time-resolved per-band cohort r (32x channels, but here we
    #            collapse across the V-axis-aligned channels) ----------
    # We compute, for each band x second, the cohort r between V-axis and the
    # mean-across-subjects-and-V-net-channels DE feature.
    # X shape: (Nsub, 28, 32, 30, 5)
    vnet_idx = [FACED_CH.index(c) for c in VNET]
    cohort_t = X.mean(axis=0)  # (28, 32, 30, 5)
    # take mean across V-net channels
    vnet_t = cohort_t[:, vnet_idx, :, :].mean(axis=1)  # (28, 30, 5)
    time_resolved_cohort = np.zeros((5, 30), dtype=np.float32)
    for bd in range(5):
        for t in range(30):
            r = np.corrcoef(vnet_t[:, t, bd], v)[0, 1]
            time_resolved_cohort[bd, t] = r
    # Best-stim trace: for each second, find the stim with highest |contribution|
    # We'll instead compute: per-band, per-second, the within-best-stim subset r
    # by using the 9-stim cohort (anger+amus+tend) which gives the strongest cohort r
    nine_idx = EMO_IDX['Anger'] + EMO_IDX['Amusement'] + EMO_IDX['Tenderness']
    time_resolved_best_stim = np.zeros((5, 30), dtype=np.float32)
    for bd in range(5):
        for t in range(30):
            r = np.corrcoef(vnet_t[nine_idx, t, bd], v[nine_idx])[0, 1]
            time_resolved_best_stim[bd, t] = r
    print(f"alpha cohort peak: t={time_resolved_cohort[2].argmax()}, r={time_resolved_cohort[2].max():.3f}")
    print(f"beta cohort peak:  t={time_resolved_cohort[3].argmax()}, r={time_resolved_cohort[3].max():.3f}")
    print(f"gamma cohort peak: t={time_resolved_cohort[4].argmax()}, r={time_resolved_cohort[4].max():.3f}")
    print(f"alpha best-stim peak: t={time_resolved_best_stim[2].argmax()}, r={time_resolved_best_stim[2].max():.3f}")

    # per-subject peak time for alpha and beta
    per_subj_t = X  # (Nsub, 28, 32, 30, 5) - already
    # per-subject vnet feature: (Nsub, 28, 30, 5)
    per_subj_vnet = per_subj_t[:, :, vnet_idx, :, :].mean(axis=2)  # (Nsub, 28, 30, 5)
    time_resolved_per_subj_peak = np.zeros((5, Nsub), dtype=np.int32)
    for bd in range(5):
        for s in range(Nsub):
            rs = np.array([np.corrcoef(per_subj_vnet[s, :, t, bd], v)[0, 1] for t in range(30)])
            time_resolved_per_subj_peak[bd, s] = int(rs.argmax())
    print("alpha per-subject peak time mean/std:",
          time_resolved_per_subj_peak[2].mean(), time_resolved_per_subj_peak[2].std())

    # ---------- (6) Connectivity matrix for V-axis network 8 channels (gamma) ----------
    # Per-subject pairwise gamma-DE correlation at second resolution, averaged
    # via Fisher-z transform across all 123 subjects.
    vnet_idx_arr = np.array([FACED_CH.index(c) for c in VNET])
    gamma_vnet = X[..., 4][:, :, vnet_idx_arr, :]  # (Nsub, 28, 8, 30)
    matrices = []
    for s in range(Nsub):
        g_flat = gamma_vnet[s].transpose(0, 2, 1).reshape(-1, len(VNET))  # (28*30, 8)
        matrices.append(np.corrcoef(g_flat.T))
    Mall = np.array(matrices)
    zall = np.arctanh(np.clip(Mall, -0.999, 0.999))
    connectivity_matrix = np.tanh(zall.mean(axis=0)).astype(np.float32)
    off_diag = connectivity_matrix[~np.eye(len(VNET), dtype=bool)]
    print(f"connectivity off-diag mean (Fisher-z) = {off_diag.mean():.3f}")
    print(f"connectivity matrix:\n{connectivity_matrix}")

    # ---------- save ----------
    np.savez(OUT,
             cohort_r_chband=cohort_r_chband,
             channels=np.array(FACED_CH),
             bands=np.array(BANDS),
             v_axis=v.astype(np.float32),
             po3_gamma_per_stim=po3_gamma_per_stim.astype(np.float32),
             per_emotion_drop_delta=per_emotion_drop_delta,
             emotions=np.array(EMOTIONS),
             drop_subset_keys=np.array(list(drop_class_table.keys())),
             drop_subset_values=np.array(list(drop_class_table.values()), dtype=np.float32),
             per_subject_simpson=per_subject_simpson,
             cohort_r_top8_fixed=np.float32(cohort_r_top8),
             per_subject_oracle_abs=per_subject_oracle_abs,
             time_resolved_cohort=time_resolved_cohort,
             time_resolved_best_stim=time_resolved_best_stim,
             time_resolved_per_subj_peak=time_resolved_per_subj_peak,
             connectivity_matrix=connectivity_matrix,
             vaxis_top8=np.array(VNET),
             top8_channels=np.array(TOP8),
             )
    print(f"Saved -> {OUT}")


if __name__ == "__main__":
    main()
