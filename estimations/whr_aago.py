from estimations.run_whr import run
from itertools import product
import os
import pandas as pd
from tqdm import tqdm
import logging

AAGO_CSV = "data/aago/aago.adapted.csv"
DIR = "estimations/whr/aago/"

os.makedirs(DIR, exist_ok=True)

HANDICAP_ELOS = range(-30, 91, 10)
DYNAMIC_FACTORS = list(map(lambda w: w**2, range(1, 11)))

EXPERIMENTS = list(product(HANDICAP_ELOS, DYNAMIC_FACTORS))


def results_path():
    return os.path.join(DIR, f"whr_aago_res.csv")


def lc_path(handicap_elo, dynamic_factor):
    return os.path.join(DIR, f"whr_aago_lc-handicap_{handicap_elo}-w2_{dynamic_factor}.csv")


def evidence_path(handicap_elo, dynamic_factor):
    return os.path.join(DIR, f"whr_aago_evidence-handicap_{handicap_elo}-w2_{dynamic_factor}.csv")


def run_with(handicap_elo, dynamic_factor):
    lc_filename = lc_path(dynamic_factor, handicap_elo)
    evidence_filename = evidence_path(dynamic_factor, handicap_elo)
    # if not os.path.exists(lc_filename) or os.path.getsize(lc_filename) == 0:
    try:
        logging.info(f'Corriendo con handicap {handicap_elo} y w2 {dynamic_factor}')
        with open(AAGO_CSV) as aago_csv:
            runner, runtime = run(aago_csv,
                                  handicap_elo=handicap_elo,
                                  dynamic_factor=dynamic_factor,
                                  day_batch=True)
            runner.learning_curves().to_csv(lc_filename, index=False)
            runner.matches_evidence().to_csv(evidence_filename, index=False)
            return {
                "geometric_mean:": runner.geometric_mean(),
                "log_evidence": runner.log_evidence(),
                "runtime": runtime
            }
    except AttributeError as err:
        logging.error(f'Handicap: {handicap_elo}, w2: {dynamic_factor}, error: {err}')


def main():
    logging.basicConfig(format='[%(levelname)s] %(asctime)s - %(message)s',
                        filename=os.path.join(DIR, 'log.log'),
                        level=logging.INFO)
    res_df = pd.read_csv(results_path())
    for handicap_elo, dynamic_factor in tqdm(EXPERIMENTS):
        stats = run_with(handicap_elo, dynamic_factor)
        if stats is not None:
            stats['handicap_elo'] = handicap_elo
            stats['dynamic_factor'] = dynamic_factor
            res_df.append(stats)
            res_df.to_csv(results_path(), index=False)


if __name__ == '__main__':
    main()
