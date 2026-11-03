# Cutaneous Galvanic Skin Conductance (EDA/GSR) Skill

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/ecosystem-OpenClaw-orange.svg)](https://openclaw.org/)
[![GenPark](https://img.shields.io/badge/sovereign-GenPark-purple.svg)](https://alphapark.ai/)
[![MCP](https://img.shields.io/badge/protocol-MCP-success.svg)](https://modelcontextprotocol.io/)

Continuous Electrodermal Activity (EDA/GSR) Tonic & Phasic Deconvolution Analyzer based on sympathetic sudomotor biophysics.

```mermaid
flowchart TD
    A[Raw Skin Conductance Series G in uS] --> B[Sliding Quantile Filter: Tonic Baseline SCL]
    A & B --> C[Phasic Subtraction: SCR = max 0, G - SCL]
    C --> D[Peak Detection & Threshold Screening > 0.05 uS]
    B & D --> E[Sympathovagal Balance & Autonomic Arousal Classification]
```

## Features
- **Zero PIP Dependencies**: Implemented strictly with Python Standard Library (`math`, `json`, `sys`, `typing`).
- **Tonic/Phasic Separation**: Isolates slow baseline drift from discrete sympathetic sweat bursts.
- **Cognitive Workload Indexing**: Quantifies autonomic arousal and acute stress events per minute.
- **Dual Architecture**: Native Python import and Model Context Protocol (MCP) JSON-RPC 2.0 stdio server.

## Quickstart
```bash
python example_usage.py
```

## License
Apache-2.0
