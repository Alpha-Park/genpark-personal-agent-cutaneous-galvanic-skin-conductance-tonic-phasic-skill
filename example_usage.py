"""
Example usage of Galvanic Skin Conductance (EDA/GSR) Tonic & Phasic Skill.
Demonstrates baseline low-arousal relaxation vs acute sympathetic stress burst sequence.
"""

import json
import math
from client import GalvanicSkinConductanceClient


def main():
    print("=== Testing Galvanic Skin Conductance (EDA/GSR) Skill ===")
    client = GalvanicSkinConductanceClient(sampling_rate_hz=10.0)

    # 1. Relaxed state: low SCL (~3.0 uS), small baseline ripple, no large SCR peaks
    relaxed_series = [
        3.0 + 0.05 * math.sin(2 * math.pi * 0.05 * (t / 10.0)) + 0.01 * (t % 3)
        for t in range(200)
    ]
    res_relaxed = client.decompose_eda(relaxed_series, scr_threshold_us=0.05)
    print("\n[Case 1: Relaxed Low-Arousal State]")
    print(json.dumps(res_relaxed, indent=2))

    # 2. Acute emotional/stress response: high SCL (~8.0 uS) with 3 prominent phasic SCR bursts
    stressed_series = []
    for t in range(200):
        # Baseline tonic drift
        val = 7.5 + 0.01 * t
        # Inject three phasic peaks at t=40 (4s), t=100 (10s), t=160 (16s)
        for peak_t, amp in [(40, 0.8), (100, 1.2), (160, 0.9)]:
            dt = t - peak_t
            if 0 <= dt <= 25:
                # Bateman-style steep rise and exponential decay
                val += amp * (dt / 5.0) * math.exp(-dt / 6.0)
        stressed_series.append(val)

    res_stressed = client.decompose_eda(stressed_series, scr_threshold_us=0.05)
    print("\n[Case 2: Acute Sympathetic Stress / High Phasic SCR Bursts]")
    print(json.dumps(res_stressed, indent=2))

    # Assertions
    assert res_relaxed["status"] == "success"
    assert res_stressed["status"] == "success"
    assert res_stressed["mean_tonic_scl_us"] > res_relaxed["mean_tonic_scl_us"]
    assert res_stressed["scr_peak_count"] >= 3
    print("\n[SUCCESS] Galvanic Skin Conductance tests passed!")


if __name__ == "__main__":
    main()
