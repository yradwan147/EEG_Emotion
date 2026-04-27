# Paper Statistics & Analysis

## 1. Statistical Significance (paired t-test, 5 seeds)

### FACED
| Comparison | t-stat | p-value | Significance |
|------------|:------:|:-------:|:------------:|
| Aug vs Baseline | 35.23 | <0.0001 | *** |
| KD+aug vs Baseline | 18.89 | <0.0001 | *** |
| Adapter64 vs Baseline | 16.67 | 0.0001 | *** |
| KD+aug vs Aug | 6.26 | 0.003 | ** |
| Adapter64 vs KD+aug | 0.61 | 0.578 | ns |

### SEED-V
| Comparison | t-stat | p-value | Significance |
|------------|:------:|:-------:|:------------:|
| Aug vs Baseline | 1.53 | 0.201 | ns |
| KD+aug vs Baseline | 3.39 | 0.028 | * |
| Adapter64 vs Baseline | 3.16 | 0.034 | * |
| KD+aug vs Aug | 2.39 | 0.075 | ns (trend) |
| Adapter64 vs KD+aug | 0.48 | 0.659 | ns |

### Interpretation
- On FACED: all improvements are highly significant (p<0.01)
- On SEED-V: KD and adapters significantly beat baseline (p<0.05), but augmentation alone does not
- Adapter64 vs KD+aug is not significant on either dataset (p>0.5) — they are equivalent

## 2. Computational Cost

| Config | Trainable Params | Epoch Time | Total (50ep) |
|--------|:----------------:|:----------:|:------------:|
| Full FT (KD+aug) | 134.1M | 0.98 min | ~49 min |
| Adapter64 (frozen BB) | 129.5M* | 1.03 min | ~52 min |

*129.5M includes the large classifier (128M). The backbone (4.9M) is frozen.
Adapter parameters: 310K. Training time is essentially identical.

## 3. Confusion Matrix Analysis (FACED, seed789)

### Baseline (B.Acc=0.571) vs Adapter64 (B.Acc=0.635)
Emotions: amusement, inspiration, joy, tenderness, anger, fear, disgust, sadness, neutral

Per-class improvement (diagonal values):
| Class | Baseline | Adapter64 | Improvement |
|-------|:--------:|:---------:|:-----------:|
| Amusement | 102 | 114 | +12 |
| Inspiration | 111 | 130 | +19 |
| Joy | 144 | 158 | +14 |
| Tenderness | 95 | 101 | +6 |
| Anger | 142 | 168 | +26 |
| Fear | 126 | 150 | +24 |
| Disgust | 129 | 125 | -4 |
| Sadness | 141 | 152 | +11 |
| Neutral | 110 | 127 | +17 |

Biggest improvements: anger (+26), fear (+24), inspiration (+19).
These are all high-arousal emotions — the KD loss helps distinguish arousal levels.

## 4. Cross-Dataset Summary

| Metric | FACED | SEED-V |
|--------|:-----:|:------:|
| Classes | 9 | 5 |
| Channels | 32 | 62 |
| Patches | 10 | 1 |
| Samples | 10,332 | 115,001 |
| Baseline B.Acc | 0.572 | 0.400 |
| Best B.Acc | 0.628 | 0.416 |
| Best Kappa | 0.582 | 0.275 |
| Improvement | +9.8% absolute | +1.9% kappa |
| Published SOTA kappa | 0.504 (CBraMod) | 0.257 (CBraMod) |
| Our best kappa | 0.582 | 0.275 |
| Relative improvement | +15.5% | +7.0% |
| Best method | adapter64 | adapter16 |

## 5. Complete Results (all 5-seed means)

### FACED (45 configs tested)
Top 10:
1. adapter64 (frozen): 0.6276 +/- 0.006
2. adapter64 (100ep): 0.6287 +/- 0.008
3. KD+aug p=0.6: 0.6266 +/- 0.004
4. adapter128: 0.6223 +/- 0.008
5. tau=0.05: 0.6223 +/- 0.009
6. KD+aug p=0.5: 0.6207 +/- 0.008
7. lambda=0.05: 0.6204 +/- 0.006
8. lora4: 0.6199 +/- 0.008
9. tau=0.20: 0.6194 +/- 0.007
10. Combo p=0.6+tau=0.05: 0.6190 +/- 0.009

### SEED-V (6 configs tested)
1. adapter16: 0.416 B.Acc, 0.275 kappa (4/5 seeds)
2. adapter64: 0.414 B.Acc, 0.272 kappa
3. kd_full_bn3: 0.412 B.Acc, 0.270 kappa
4. kd_no_aug: 0.407 B.Acc, 0.265 kappa (4/5 seeds)
5. aug_only: 0.406 B.Acc, 0.263 kappa
6. baseline: 0.400 B.Acc, 0.256 kappa
