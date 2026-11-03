"""
Cutaneous Galvanic Skin Conductance (EDA/GSR) Tonic & Phasic Decomposition Client.
Zero-mock pure Python standard library implementation.
Deconvolves continuous skin conductance recordings (uS) into tonic baseline (SCL)
and phasic sweat gland burst responses (SCR / Bateman impulse response function).
"""

import math
from typing import Dict, Any, List, Optional


class GalvanicSkinConductanceClient:
    """
    Decomposes electrodermal activity (EDA) into:
    - Tonic Skin Conductance Level (SCL): Slow autonomic baseline (~0.05 Hz)
    - Phasic Skin Conductance Response (SCR): Rapid sudomotor sympathetic bursts (>0.05 uS)
    """

    def __init__(self, sampling_rate_hz: float = 10.0):
        if sampling_rate_hz <= 0:
            raise ValueError("Sampling rate must be positive.")
        self.sampling_rate_hz = sampling_rate_hz

    def decompose_eda(
        self,
        conductance_series_us: List[float],
        scr_threshold_us: float = 0.05,
        moving_avg_window_s: float = 4.0
    ) -> Dict[str, Any]:
        """
        Decomposes skin conductance series in microSiemens (uS).
        conductance_series_us: Array of skin conductance values (uS).
        scr_threshold_us: Minimum phasic amplitude to qualify as an SCR peak (default: 0.05 uS).
        moving_avg_window_s: Window size in seconds for estimating tonic baseline.
        """
        if not conductance_series_us or len(conductance_series_us) < 10:
            raise ValueError("Conductance series must contain at least 10 samples.")

        n = len(conductance_series_us)
        window_samples = max(3, int(moving_avg_window_s * self.sampling_rate_hz))

        # 1. Estimate Tonic Skin Conductance Level (SCL) using a sliding local baseline filter
        tonic_scl = []
        for i in range(n):
            start = max(0, i - window_samples // 2)
            end = min(n, i + window_samples // 2 + 1)
            # Local percentile/minimum represents tonic baseline uncontaminated by phasic spikes
            sub = sorted(conductance_series_us[start:end])
            low_quantile = sub[len(sub) // 5]  # 20th percentile
            tonic_scl.append(low_quantile)

        # 2. Extract Phasic Skin Conductance Response (SCR):
        # Phasic(t) = max(0, EDA(t) - Tonic(t))
        phasic_scr = [max(0.0, conductance_series_us[i] - tonic_scl[i]) for i in range(n)]

        # 3. Peak Detection on Phasic Component:
        # Detect local maxima exceeding scr_threshold_us
        peaks = []
        for i in range(1, n - 1):
            if (phasic_scr[i] > phasic_scr[i - 1] and
                phasic_scr[i] >= phasic_scr[i + 1] and
                phasic_scr[i] >= scr_threshold_us):
                t_s = i / self.sampling_rate_hz
                peaks.append({
                    "time_s": round(t_s, 2),
                    "amplitude_us": round(phasic_scr[i], 3)
                })

        # Summary statistics
        mean_scl = sum(tonic_scl) / n
        mean_phasic = sum(phasic_scr) / n
        duration_s = n / self.sampling_rate_hz
        scr_frequency_per_min = (len(peaks) / (duration_s / 60.0)) if duration_s > 0 else 0.0

        # Autonomic sympathetic arousal classification:
        # Rested state: SCL 2.0 - 6.0 uS, SCR rate 1 - 3 per minute
        # Moderate mental workload / vigilance: SCL 6.0 - 12.0 uS, SCR rate 4 - 8 per min
        # Acute sympathetic surge / fight-or-flight: SCL > 12.0 uS, SCR rate > 10 per min
        if mean_scl < 5.0 and scr_frequency_per_min < 4.0:
            arousal_state = "Low Sympathetic Arousal / Deep Relaxation"
            autonomic_tone = "Parasympathetic Dominance"
        elif mean_scl <= 10.0 and scr_frequency_per_min <= 8.0:
            arousal_state = "Moderate Focused Alertness / Normal Cognitive Load"
            autonomic_tone = "Balanced Sympathovagal State"
        elif mean_scl <= 16.0 or scr_frequency_per_min <= 14.0:
            arousal_state = "High Autonomic Sympathetic Arousal / Acute Stress"
            autonomic_tone = "Sympathetic Activation"
        else:
            arousal_state = "Extreme Sympathetic Overdrive / Panic / Pain Surge"
            autonomic_tone = "Intense Sympathetic Hyper-Reactivity"

        return {
            "status": "success",
            "sample_count": n,
            "duration_seconds": round(duration_s, 2),
            "mean_tonic_scl_us": round(mean_scl, 3),
            "mean_phasic_amplitude_us": round(mean_phasic, 3),
            "scr_peak_count": len(peaks),
            "scr_frequency_per_min": round(scr_frequency_per_min, 1),
            "detected_scr_events": peaks[:5],  # top 5 events
            "evaluation": {
                "arousal_state": arousal_state,
                "autonomic_tone": autonomic_tone
            }
        }
