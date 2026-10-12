import argparse
import csv
import math
import random

FIELDS = ['seed', 'n', 'crossings', 'pi_estimate', 'needle_length', 'line_spacing']


def _geometry(length, spacing):
    if not (math.isfinite(length) and math.isfinite(spacing) and 0 < length <= spacing):
        raise ValueError('Require finite 0 < length <= spacing')


def _count(n):
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError('n must be a positive integer')


def crosses_line(distance, angle, length=0.5, spacing=1.0):
    _geometry(length, spacing)
    if not (0 <= distance <= spacing / 2 and 0 <= angle <= math.pi / 2):
        raise ValueError('distance or angle outside allowed range')
    return distance <= length / 2 * math.sin(angle)


def estimate_pi(n, crossings, length=0.5, spacing=1.0):
    _geometry(length, spacing)
    _count(n)
    if isinstance(crossings, bool) or not isinstance(crossings, int) or not 0 < crossings <= n:
        raise ValueError('crossings must be an integer in [1, n]')
    return 2 * length * n / (spacing * crossings)


def simulate(n, seed=42, length=0.5, spacing=1.0):
    _geometry(length, spacing)
    _count(n)
    rng = random.Random(seed)  # Once per independent experiment, outside the loop.
    crossings = 0
    for _ in range(n):
        distance = rng.uniform(0, spacing / 2)
        angle = rng.uniform(0, math.pi / 2)
        crossings += crosses_line(distance, angle, length, spacing)
    return dict(zip(FIELDS, [seed, n, crossings, estimate_pi(n, crossings, length, spacing), length, spacing]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    rows = [simulate(n, seed=args.seed) for n in (1000, 10000, 100000)]
    with open('results.csv', 'w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(row)


if __name__ == '__main__':
    main()
