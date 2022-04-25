import os
from math import exp
import numpy as np
import pandas as pd

from estimations.whr_aago import EXPERIMENTS, evidence_path, results_path


def load_df(handicap_elo, dynamic_factor, handicap_elo_offset):
    path = evidence_path(handicap_elo, dynamic_factor, handicap_elo_offset)
    if os.path.isfile(path):
        return pd.read_csv(path)


def main():
    dfs = [
        (handicap_elo, dynamic_factor, handicap_elo_offset, load_df(handicap_elo, dynamic_factor, handicap_elo_offset))
        for handicap_elo, dynamic_factor, handicap_elo_offset in EXPERIMENTS
    ]

    data = pd.DataFrame([
        (handicap_elo, dynamic_factor, handicap_elo_offset, np.log(df['evidence']).sum(), exp(np.log(df['evidence']).mean()))
        for handicap_elo, dynamic_factor, handicap_elo_offset, df in dfs
        if df is not None
    ], columns=['handicap_elo', 'dynamic_factor', 'handicap_elo_offset', 'log_evidence', 'geometric_mean'])
    data.to_csv(results_path(), index=False)


if __name__ == '__main__':
    main()
