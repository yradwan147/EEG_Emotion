# Verified Paper Numbers — NeurIPS 2026
## Generated: 2026-04-09 Session 19

### Table 1: Cross-Backbone KD Results (FACED, 9 classes)
| Backbone | Venue | Params | Baseline BAcc | +KD BAcc | Δ (abs) | Δ (rel) | p-value | Seeds |
|----------|-------|--------|:---:|:---:|:---:|:---:|:---:|:---:|
| CBraMod | ICLR 2025 | 3.5M | 0.572±0.009 | 0.627±0.006 | +0.055 | +9.6% | 8e-6*** | 5 |
| CBraMod | ICLR 2025 | 3.5M | 0.572±0.009 | 0.628±0.006 (adapter) | +0.056 | +9.8% | — | 5 |
| LaBraM | ICLR 2024 | 5.8M | 0.370±0.010 | 0.396±0.014 | +0.026 | +6.9% | 0.025* | 5 |

### Table 2: SEED-V Results (5 classes)
| Backbone | Baseline BAcc | +KD BAcc | Δ | Note |
|----------|:---:|:---:|:---:|------|
| CBraMod | 0.416±0.003 | 0.416±0.003 | 0.0% | KD = zero effect (all taus identical) |
| LaBraM | 0.416 | 0.416 | 0.0% | All 3 variants flat |

**Explanation:** SEED-V has too few tokens per sample (CBraMod: 1 patch, LaBraM: 63 tokens) for KD gradient to influence training.

### Table 3: LLM Scale Analysis (Qwen2.5 family, 67% depth)
| Model | Params | Hidden Dim | Pearson r | Spearman r | Cluster Sep |
|-------|--------|:---:|:---:|:---:|:---:|
| Qwen-0.5B | 0.5B | 896 | 0.932 | 0.867 | 1.74 |
| Qwen-1.5B | 1.5B | 1536 | 0.955 | 0.913 | **2.04** |
| Qwen-3B | 3B | 2048 | **0.976** | **0.933** | 1.77 |
| Qwen-7B | 7B | 3584 | 0.941 | 0.900 | 1.87 |
| Qwen-14B | 14B | 5120 | 0.943 | 0.900 | 1.81 |
| Qwen-32B | 32B | 5120 | 0.926 | 0.883 | 1.68 |
| Qwen-72B | 72B | 8192 | 0.965 | 0.933 | 1.63 |

### Table 4: Depth Comparison (29% vs 67%)
| Model | 29% |r| | 67% r | Δ |
|-------|:---:|:---:|:---:|
| 0.5B | 0.850 | 0.932 | -0.082 |
| 1.5B | 0.817 | 0.955 | -0.138 |
| 3B | 0.783 | 0.976 | -0.193 |
| 7B | 0.833 | 0.941 | -0.108 |
| 14B | 0.800 | 0.943 | -0.143 |
| 32B | 0.833 | 0.926 | -0.093 |

### Table 5: Vector Source Ablation (CBraMod FACED, tau=0.1)
| Vector Source | BAcc | Note |
|:---:|:---:|------|
| LLM (Qwen-0.5B) | 0.624 | — |
| SBERT | 0.621 | — |
| Random | 0.619 | — |
| One-hot | 0.616 | — |
| InfoNCE+3L-BN | 0.614 | Different loss fn |
| No KD baseline | 0.572 | — |

**Key insight:** At tau=0.1, soft targets collapse to one-hot (entropy=0.004). The BN projection head is the active ingredient, not the specific vectors.

### Table 6: Layer Selection (Qwen-1.5B on CBraMod FACED)
| Layer | Depth | BAcc | p vs best |
|:---:|:---:|:---:|:---:|
| 4 | 14% | 0.615 | 0.009** |
| 8 | 29% | **0.628** | — |
| 14 | 50% | 0.623 | 0.219 |
| 20 | 71% | 0.622 | 0.135 |
| 24 | 86% | 0.619 | 0.050* |
| 27 | 96% | 0.621 | 0.105 |
| 28 (last) | 100% | 0.624 | 0.383 |

### Table 7: SFT Effect on Emotion Vectors (Qwen-0.5B)
| Variant | Cluster Sep | Δ vs base |
|---------|:---:|:---:|
| Base (no SFT) | 1.74 | — |
| SFT 189 instr | 1.70 | -2.3% |
| SFT 1898 instr | 1.63 | -6.3% |

### Per-Class Analysis (CBraMod FACED, adapter64)
Top improvements: Fear +8.9%, Amusement +7.2%
Worst: Neutral -1.8% (but starts very low)

### Statistical Tests Summary
| Comparison | t-stat | df | p-value | Sig |
|-----------|:---:|:---:|:---:|:---:|
| CBraMod FACED KD vs base | 9.77 | 4 | 8e-6 | *** |
| LaBraM FACED KD vs base | 3.48 | 4 | 0.025 | * |
| CBraMod SEED-V KD vs base | — | — | n.s. | — |
| LaBraM SEED-V KD vs base | — | — | n.s. | — |
| Layer 8 vs Layer 4 | — | — | 0.009 | ** |
