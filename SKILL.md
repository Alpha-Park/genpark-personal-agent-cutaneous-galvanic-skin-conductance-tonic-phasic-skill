---
name: genpark-personal-agent-cutaneous-galvanic-skin-conductance-tonic-phasic-skill
description: Tonic and Phasic Electrodermal Activity (EDA) / Galvanic Skin Response (GSR) decomposition analyzer. Deconvolves continuous skin conductance into slow tonic SCL and fast phasic SCR peaks.
version: 1.0.0
author: GenPark Ecosystem
license: Apache-2.0
tags:
  - personal-agent
  - eda
  - gsr
  - sympathetic
  - autonomic
  - stress
  - openclaw
  - genpark
  - mcp
---

# Cutaneous Galvanic Skin Conductance (EDA/GSR) Skill

## Overview
This skill decomposes continuous electrodermal activity recordings into its two distinct physiological components:
- **Tonic Skin Conductance Level (SCL)**: Slow, drifting baseline governed by background sudomotor sympathetic tone and stratum corneum hydration.
- **Phasic Skin Conductance Responses (SCR)**: Rapid transient conductance spikes ($\approx 1-3\text{ s}$ rise, $2-10\text{ s}$ recovery) reflecting burst firing of post-ganglionic sympathetic sudomotor nerve fibers in response to acute emotional, cognitive, or physical arousal.

## Mathematical Formulation
1. **Tonic Baseline Estimation**:
   $$\text{SCL}(t) = \text{Quantile}_{0.20}\left(\{G(\tau) \mid t - W/2 \le \tau \le t + W/2\}\right)$$
2. **Phasic Extraction**:
   $$\text{SCR}(t) = \max(0, G(t) - \text{SCL}(t))$$
3. **Phasic Peak Criterion**:
   $$\text{Peak} = \{t \mid \text{SCR}(t) > \text{SCR}(t-1) \text{ and } \text{SCR}(t) \ge \text{SCR}(t+1) \text{ and } \text{SCR}(t) \ge \theta_{\text{SCR}}\}$$
4. **SCR Frequency**:
   $$\text{Rate} = \frac{N_{\text{peaks}}}{\text{Duration (minutes)}}$$

## Usage
```python
from client import GalvanicSkinConductanceClient

client = GalvanicSkinConductanceClient(sampling_rate_hz=10.0)
res = client.decompose_eda(
    conductance_series_us=[4.2, 4.3, 4.5, 5.1, 5.8, 5.2, 4.4, ...],
    scr_threshold_us=0.05
)
print(res["evaluation"]["arousal_state"])
```
