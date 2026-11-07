# Cross-Platform Game Testing Companion

Runnable companion for the [Cross-Platform Game Testing Guide](https://qapractices.com/documentation/cross-platform-game-testing/) — small utilities for the guide's performance and certification sections: a frame-time analyzer, a sample capture, a pre-cert checklist in YAML, and an adb thermal-monitoring script.

## Run

```bash
python frame_time_report.py frame_times_sample.csv
```

Python 3.12+ required; stdlib only. Expected output against the bundled capture:

```text
frames: 360 | avg fps: 55.7 | 1% low: 22.1 | stutters: 19
```

The thermal logger needs a connected Android device:

```bash
./thermal_log.sh 1800 thermal_log.csv   # 30-minute sustained session
adb shell dumpsys gfxinfo <package> framestats  # pair with frame times
```

## What it covers

| File | Guide section | What it proves |
|---|---|---|
| `frame_time_report.py` | Performance Testing | Average fps, 1% low, and stutter frames (>33 ms) from a raw capture |
| `frame_times_sample.csv` | Performance Testing | 360-frame capture: ~60 fps stream with realistic pacing spikes |
| `cert-checklist.yaml` | Certification and Store Compliance | Pre-submission checks: suspend/resume, input, storage, errors, storefront, achievements |
| `thermal_log.sh` | Thermal throttling | Max thermal-zone temperature sampled every 5 s during a session |
