# Threat Modeling for QA Engineers — Companion Files

Runnable PyTM 1.3 threat model for a checkout service, matching the worked example in the [Threat Modeling for QA Engineers](https://qapractices.com/documentation/threat-modeling-for-qa-engineers/) guide.

## Files

- `threat_model.py` — PyTM model: three trust boundaries (Internet, DMZ, Internal), a customer → web app → API → orders DB flow, with `storesPII` flagged on the datastore so STRIDE analysis flags information-disclosure threats.
- `requirements.txt` — pinned `pytm` version.

## Run

```bash
pip install -r requirements.txt

# STRIDE threat report (markdown)
python threat_model.py --report report.md

# Data flow diagram (requires Graphviz `dot` on PATH)
python threat_model.py --dfd | dot -Tpng -o dfd.png
```

The report lists threats per element — each row maps to a STRIDE category (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege). QA's job: turn each high-risk threat into a test case and keep the threat-ID traceability in the suite.
