import csv
import math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    with open('results.csv', encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError('results.csv has no experiments')
    ns = [int(row['n']) for row in rows]
    estimates = [float(row['pi_estimate']) for row in rows]
    table = [r'\begin{tabular}{rrr}', r'\toprule', r'投针数 $N$ & 相交数 $K$ & $\widehat{\pi}$ \\', r'\midrule']
    params = []
    for row in rows:
        n, k = int(row['n']), int(row['crossings'])
        length, spacing = float(row['needle_length']), float(row['line_spacing'])
        value = float(row['pi_estimate'])
        if not math.isclose(value, 2 * length * n / (spacing * k), rel_tol=1e-12):
            raise ValueError('CSV estimate does not match its recorded counts')
        table.append(f'{n} & {k} & {value:.6f} ' + r'\\')
        params.append(f"$N={n}$：seed={int(row['seed'])}，针长 $L={length:g}$，线距 $d={spacing:g}$。")
    table.extend([r'\bottomrule', r'\end{tabular}'])
    Path('results-table.tex').write_text('\n'.join(table) + '\n', encoding='utf-8')
    Path('results-params.tex').write_text('\n\n'.join(params) + '\n', encoding='utf-8')
    first, last = estimates[0], estimates[-1]
    observation = f'本次实验中，投针数从 {ns[0]} 增至 {ns[-1]} 时，估计值从 {first:.6f} 变为 {last:.6f}，绝对误差分别为 {abs(first-math.pi):.6f} 和 {abs(last-math.pi):.6f}。这是本次固定种子下的观察，不代表样本数增加时误差必定单调减小。'
    Path('results-observation.tex').write_text(observation + '\n', encoding='utf-8')
    fig, ax = plt.subplots(figsize=(7.2, 3.4), layout='constrained')
    ax.plot(ns, estimates, 'o-', label='Buffon estimate')
    ax.axhline(math.pi, linestyle='--', color='gray', label='Reference pi')
    ax.set_xscale('log')
    ax.set_xticks(ns, labels=[str(n) for n in ns])
    ax.set_xlabel('Number of throws (N)')
    ax.set_ylabel('Estimated pi')
    ax.grid(alpha=0.25)
    ax.legend()
    fig.savefig('results.png', dpi=180)
    plt.close(fig)
    print('Generated table, parameters, observation and results.png from results.csv')


if __name__ == '__main__':
    main()
