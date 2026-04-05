# Number Audit — Every Number in the Paper Mapped to Source

## Abstract
| Number | Source |
|--------|--------|
| 0.628 B.Acc | worklog.md: adapter64 mean = 0.6276 |
| +11.2% over REVE | (0.6276 - 0.5646) / 0.5646 = 11.15% |
| kappa = 0.275 | worklog.md: SEED-V adapter16 kappa mean |
| +7.0% over CBraMod | (0.275 - 0.257) / 0.257 = 7.0% |
| 310K params | model_enhanced.py: adapter64 = 12 layers x (200x64 + 64x200) = 307,200 |
| 4.9M params | CBraMod backbone parameter count |
| 45 configs | Count of unique experiment configurations in worklog |
| 400+ runs | Total individual training runs across all experiments |
| p < 0.001 | paper_statistics.md: FACED LOSO adapter64 p=0.0004 |
| 6 families | Qwen, Mistral, Phi-2, TinyLlama, Pythia, Bloom |

## Table 1 (Main Results)
| Number | Source |
|--------|--------|
| CBraMod paper 0.551 | CBraMod paper (ICLR 2025), arXiv:2412.07236 |
| LaBraM kappa 0.470 | CBraMod paper Table comparing with LaBraM |
| REVE 0.565 | REVE paper, arXiv:2510.21585 |
| CBraMod repro 0.572 | paper_clean baseline_seed*/epoch*.pth, 5-seed mean |
| Aug only 0.609 | paper_clean aug_seed*/epoch*.pth, 5-seed mean |
| KD+aug 0.627 | kd_sweep aug06_seed*, 5-seed mean |
| Adapter64 0.628 | arch_phase1 adapter64_seed*/epoch*.pth, 5-seed mean |
| SEED-V baseline 0.400 | seedv baseline seeds, 5-seed mean |
| SEED-V adapter 0.416 | seedv adapter16 seeds, 5-seed mean |
| SEED-V kappa 0.275 | seedv adapter16 kappa, 5-seed mean |

## Table 2 (LOSO)
| Number | Source |
|--------|--------|
| Baseline fold means | loso/logs/loso_46374675_*.out: grep "model save" |
| KD fold means | Same logs, mode=kd_full_bn3 |
| Adapter fold means | Same logs, mode=adapter64 |
| p=0.0002 | paper_statistics.md: paired t-test |
| p=0.0004 | paper_statistics.md: paired t-test |

## Augmentation Ablation (Table)
| Number | Source |
|--------|--------|
| 0.609 full aug | aug_ablation logs, no_noise/no_jitter/etc seeds, 5-seed means |
| 0.569 drop jitter | aug_ablation no_jitter seeds |
| -3.9% | 0.609 - 0.569 = 0.040 |

## KD Sweep (Table)
| Number | Source |
|--------|--------|
| All lambda/tau/augp values | kd_sweep logs kd_sweep_46360279_*.out |

## Error Pattern
| Number | Source |
|--------|--------|
| r=0.38, p=3.4e-6 | reports/error_pattern_controls_report.md |
| 64.6%, p=3.2e-13 | Same report, within-negative analysis |

## Per-Subject
| Number | Source |
|--------|--------|
| 78% improve | experiments/analysis/per_subject_results.json: 18/23 > 0.01 |
| +3.8% mean | Same file: mean delta |
| +15.1% max | Same file: subject 5 |
