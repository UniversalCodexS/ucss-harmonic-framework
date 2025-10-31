# UCSS Harmonic Framework v0.1

**Verification of Truth Through Spectral Compression and Regeneration**

This repository demonstrates how spectral decomposition can both compress and verify information integrity using truncated Fourier bases.

A synthetic waveform dataset was analyzed across variable harmonic counts (K = 20, 80, all).  
Partial reconstructions maintained amplitude and phase coherence while reducing stored spectral data by 6×–25×.  
Full reconstruction (K = all) achieved bit-perfect equivalence verified through SHA-256 checksum alignment.

---

### 📂 Contents

- `waveform_demo.py` — Generates the initial synthetic waveform.
- `ucss_demo_compress_regen.py` — Demonstrates harmonic compression and reconstruction.
- `/figures/` — Output graphs for each K value (20, 80, all).
- `/paper/` — Research findings and DOI reference.

---

### 🧮 Summary

**Key Findings**
- Harmonic compression preserves coherent reconstruction across major frequency bins.
- Complete spectral restoration achieves checksum-verified identity preservation.
- Demonstrates mathematically reversible compression under bounded entropy.

**Compression Ratios**
| Harmonic Count (K) | Approx. Reduction | Bit-Perfect |
|--------------------:|------------------:|-------------:|
| 20 | ~25× smaller | ❌ |
| 80 | ~6× smaller | ❌ |
| all | 1× (original) | ✅ |

---

### 🧾 Citation

Hedges, D. (2025). *UCSS Harmonic Framework v0.1 — Verification of Truth Through Spectral Compression and Regeneration*.  
Zenodo. [https://doi.org/10.5281/zenodo.17494221](https://doi.org/10.5281/zenodo.17494221)

---

### 🧠 License

Released under **MIT License** for educational and verification purposes only.  
All conceptual rights to the Universal Codex Systems and Solutions (UCSS) remain reserved.
