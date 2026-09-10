#!/usr/bin/env python3
"""Assert SLA from JMeter JTL results. Fails CI if p95 or error rate exceed thresholds.

Usage:
    python assert-sla.py --jtl results/checkout.jtl --max-p95 1000 --max-error-rate 0.5
"""
import csv
import argparse
import sys

parser = argparse.ArgumentParser(description='Assert SLA from JMeter JTL results')
parser.add_argument('--jtl', required=True, help='Path to JTL results file')
parser.add_argument('--max-p95', type=int, required=True, help='Maximum p95 in ms')
parser.add_argument('--max-error-rate', type=float, required=True, help='Maximum error rate percentage')
args = parser.parse_args()

rows = list(csv.DictReader(open(args.jtl)))
if not rows:
    sys.exit('No results found')

total = len(rows)
errors = sum(1 for r in rows if r['success'] != 'true')
error_rate = (errors / total) * 100
sorted_times = sorted(int(r['elapsed']) for r in rows)
p95 = sorted_times[int(total * 0.95)]

print(f'Samples: {total}, p95: {p95} ms, error rate: {error_rate:.2f}%')

if p95 > args.max_p95:
    sys.exit(f'p95 {p95} ms exceeds {args.max_p95} ms')
if error_rate > args.max_error_rate:
    sys.exit(f'Error rate {error_rate:.2f}% exceeds {args.max_error_rate}%')
