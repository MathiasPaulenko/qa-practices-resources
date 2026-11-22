# Chaos Engineering Experiment Template — Companion

Downloadable files for the [Chaos Engineering Experiment Template](https://qapractices.com/templates/chaos-engineering-experiment-template/) on QAPractices.

## Contents

| File | Purpose |
|---|---|
| `chaos-engineering-experiment-template.md` | Blank experiment document: details, hypothesis, blast radius control, steady-state metrics, injection plan, abort conditions, results, findings and sign-off. |
| `experiment-ce-042-sample.md` | The same document filled for CE-042, a pod-kill experiment on a Kubernetes API gateway — hypothesis partially failed, two findings with owners. |
| `pod-kill.yaml` | Chaos Mesh 2.7 PodChaos manifest that terminates 30% of `api-gateway` pods for one minute; the injection step from the sample. |

## Usage

1. Copy `chaos-engineering-experiment-template.md` into your project docs or wiki and fill Sections 1-6 before the run — never from memory afterwards.
2. Adapt `pod-kill.yaml` to your selector (`app` label, namespace) and blast radius, then apply it with `kubectl apply -f pod-kill.yaml`.
3. Pause the injection at any time with `kubectl annotate podchaos <name> experiment.chaos-mesh.org/pause=true` — rehearse this before the first real run.
4. Use `experiment-ce-042-sample.md` as the reference for how a falsifiable hypothesis and honest findings look when the experiment doesn't fully pass.

Requires [Chaos Mesh](https://chaos-mesh.org/) installed on the target cluster for the YAML; the document itself is tool-agnostic.
