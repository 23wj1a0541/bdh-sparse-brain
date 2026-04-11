# 🐉 BDH Sparse Brain — Post-Transformer Visualization

> **Post-Transformer Hackathon by Pathway | IIT Ropar**
> Path A: Visualization and Inner Worlds

![BDH vs Transformer Activation](https://img.shields.io/badge/Architecture-Post--Transformer-1D9E75?style=flat-square)
![Track](https://img.shields.io/badge/Track-Visualization-7F77DD?style=flat-square)
![Status](https://img.shields.io/badge/Demo-Live-brightgreen?style=flat-square)

---

## What We Built

**BDH Sparse Brain** is an interactive side-by-side visualization that makes the Dragon Hatchling's most striking architectural property visceral and immediately understandable: its ~5% sparse neuron activation, compared to a Transformer's ~95% dense activation, on the exact same input token.

Users type any word — "currency", "Paris", "medicine" — and watch two neural grids respond in real time. BDH lights up a sparse constellation of neurons; the Transformer floods with near-uniform activity. A live layer-by-layer density chart makes the contrast quantitative. The difference is not subtle. It is the point.

This visualization targets the 30% of judging weight allocated to **visual clarity for non-experts** — a researcher, engineer, or executive should understand BDH's efficiency advantage within seconds of interacting with it.

---

## What Insight It Reveals About BDH

The Dragon Hatchling paper (Section 6.4) establishes that roughly **5% of neurons fire per token** in BDH, compared to near-100% activation in transformers. This is not a result of pruning, distillation, or L1 regularization — it emerges naturally from the architecture's sparse ReLU activations.

This visualization makes three things tangible:

1. **Efficiency**: Fewer active neurons = less compute per token. The visual contrast makes this obvious without reading a paper.
2. **Interpretability**: When only 5% of neurons matter for a given input, you can actually trace what happened. The paper demonstrates "currency synapses" and "country synapses" — monosemantic encoding that transformers cannot achieve. Our visualization shows *why* that's possible: there are only a few neurons to inspect.
3. **The paradigm shift**: Seeing both architectures respond to the same token side-by-side communicates in one frame what takes paragraphs to explain in text.

---

## Live Demo

🌐 **[View Live Demo →](https://23wj1a0541.github.io/bdh-sparse-brain/)**

> Replace with your HuggingFace Space or GitHub Pages URL after deployment.

---

## Demo Video

🎬 **[Watch 2-Minute Demo on YouTube →](https://youtu.be/_prz4NoVE18)**

> Replace with your unlisted YouTube link after recording.

---

## How to Run Locally

No build step. No dependencies. No server required.

```bash
git clone https://github.com/your-username/bdh-sparse-brain
cd bdh-sparse-brain
open index.html   # macOS
# or double-click index.html on Windows/Linux
```

That's it. The entire visualization runs in-browser.

---

## Project Structure

```
bdh-sparse-brain/
├── index.html          # Complete self-contained visualization (no build needed)
├── README.md           # This file
└── assets/
    └── demo-preview.png  # Screenshot for README (add after recording)
```

---

## Technical Architecture

### Frontend
- **Pure HTML/CSS/JavaScript** — zero build toolchain, zero npm, zero dependencies to install
- **Chart.js 4.4.1** (loaded via CDN) for the layer-by-layer density line chart
- **Canvas API** for the neuron grid heatmaps — each cell is a neuron, brightness encodes activation strength
- **Google Fonts** — Fraunces (display) + DM Sans (body) — matching Vidyasetu brand palette

### Activation Modeling
The simulated activations are modeled directly on BDH paper findings:
- **BDH**: ~5% sparsity per layer (Section 6.4 of the paper — "roughly 5% of neurons fire")
- **Transformer**: ~93–95% activation density (dense, near-uniform)
- Activation values are seeded from the input token string, so the same word always produces the same pattern — the visualization is deterministic and consistent
- Layer-by-layer density shows how sparsity is maintained across depth, not just in one layer

### Next Phase (Round 2 Integration)
The current prototype uses analytically-modeled activations. The full implementation will:
1. Run actual BDH inference via the [official repository](https://github.com/pathwaycom/bdh)
2. Extract real activation tensors using hooks on the sparse ReLU layers
3. Stream activations to the frontend via a lightweight FastAPI/Flask backend
4. Add Hebbian synapse strengthening animation — showing σ matrix weights evolve as tokens are processed

---

## Roadmap

| Feature | Status |
|---|---|
| Side-by-side neuron grid (BDH vs Transformer) | ✅ Complete |
| Layer density line chart | ✅ Complete |
| Token-seeded deterministic patterns | ✅ Complete |
| Adjustable neuron count slider | ✅ Complete |
| Real BDH inference backend | 🔄 In Progress |
| Hebbian learning animator (σ matrix evolution) | 📋 Planned |
| Graph topology explorer (G_x = E @ D_x) | 📋 Planned |
| Monosemanticity dashboard (synapse concept probing) | 📋 Planned |
| Export activation patterns as PNG/GIF | 📋 Planned |

---

## Alignment With Judging Criteria

| Criterion | Weight | How We Address It |
|---|---|---|
| Visual clarity for non-experts | 30% | Core design goal — contrast is immediate, no ML knowledge needed |
| Technical correctness | 25% | Activation densities match paper Section 6.4 findings precisely |
| Insight into architecture | 25% | Reveals *why* BDH is interpretable — sparse = traceable |
| Presentation quality | 20% | Polished UI, responsive, live demo, video walkthrough |

---

## About BDH

The Dragon Hatchling (BDH) is a post-transformer architecture by [Pathway](https://pathway.com) that solves fundamental transformer limitations:

| Property | Transformer | BDH |
|---|---|---|
| Activation density | ~100% of neurons | ~5% of neurons |
| Memory | KV-cache (grows with context) | Hebbian synapses (constant size) |
| Attention complexity | O(T²) | O(T) linear |
| Interpretability | Black box | Graph structure + monosemantic synapses |
| Learning | Frozen at training | Continues at inference |

**Paper**: [arxiv.org/abs/2509.26507](https://arxiv.org/abs/2509.26507) — #1 paper on HuggingFace the month it was published, #2 paper of 2025.

---

## Resources Used

- [Official BDH Repository](https://github.com/pathwaycom/bdh)
- [BDH Research Paper](https://arxiv.org/abs/2509.26507)
- [krychu/bdh visualization reference](https://github.com/krychu/bdh)
- [Transformer Explainer (Georgia Tech)](https://poloclub.github.io/transformer-explainer) — inspiration
- [Pathway Official Site](https://pathway.com)

---

## Team

| Name | Role |
|---|---|
| [Kuldeep Reddy] | ML Architecture |
| [Arun Sai Challa] | Front-End |
| [Abhinav Gajavelli] |  Visualization |
| [Mahesh Bommagani] | Research |

> *Built for the Post-Transformer Hackathon by Pathway at IIT Ropar*

---

## Limitations & Future Scope

**Current limitations:**
- Activation data is analytically modeled from paper statistics, not extracted from live BDH inference. The patterns are accurate in density (~5% vs ~95%) but are not token-specific in the way real BDH activations would be.
- The Transformer comparison uses simulated dense activations — a real side-by-side would require running GPT-2 inference alongside BDH.
- No persistent state across sessions — Hebbian synapse strengthening is not yet animated.

**Future scope:**
- Integrate live BDH inference backend to show real activation tensors
- Add Hebbian learning animation showing the σ matrix evolve over a sequence
- Build the graph topology explorer showing the scale-free hub structure of G_x
- Implement monosemanticity probing — click any synapse, see what concept it encodes
- Compare memory usage curves: BDH flat O(1) vs Transformer growing KV-cache

---

## License

MIT License — feel free to build on this work.  