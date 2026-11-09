import json, sys, numpy as np
sys.path.insert(0,'/ibex/project/c2323/yousef/EEG_Emotion/figures/landmark/scripts')
RB='/ibex/project/c2323/yousef/reports/rebuttal_2026_11'
OUT='/ibex/project/c2323/yousef/EEG_Emotion/figures/landmark'
W=json.load(open(f'{RB}/wave2b_analysis.json'))
TAGS=W['e150_tags']; A=W['A']
R={t:json.load(open(f'{RB}/resdiag_trainfit/resdiag_{t}.json')) for t in TAGS}
orig=np.array([not t.startswith('rb_') for t in TAGS])
assert orig.sum()==5 and len(TAGS)==20
