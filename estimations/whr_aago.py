from estimations.run_whr import run
from itertools import product
import os
from tqdm import tqdm
import logging

AAGO_CSV = "data/aago/aago.adapted.csv"
DIR = "estimations/whr/aago/"

os.makedirs(DIR, exist_ok=True)

HANDICAP_ELOS = range(0, 251, 25)
DYNAMIC_FACTORS = list(map(lambda w: w**2, range(1, 11)))

EXPERIMENTS = list(product(HANDICAP_ELOS, DYNAMIC_FACTORS))


def run_with(handicap_elo, dynamic_factor):
    lc_filename = os.path.join(DIR, f"whr_aago_lc-handicap_{handicap_elo}-w2_{dynamic_factor}.csv")
    res_filename = os.path.join(DIR, f"whr_aago_res-handicap_{handicap_elo}-w2_{dynamic_factor}.txt")
    if not os.path.exists(lc_filename) or os.path.getsize(lc_filename) == 0:
        try:
            logging.info(f'Corriendo con handicap {handicap_elo} y w2 {dynamic_factor}')
            with open(AAGO_CSV) as aago_csv, open(lc_filename, "w") as lc, open(res_filename, "w") as res:
                run(aago_csv, lc, res,
                    handicap_elo=handicap_elo,
                    dynamic_factor=dynamic_factor,
                    day_batch=True)
        except AttributeError as err:
            logging.error(f'Handicap: {handicap_elo}, w2: {dynamic_factor}, error: {err}')


def main():
    logging.basicConfig(format='[%(levelname)s] %(asctime)s - %(message)s',
                        filename=os.path.join(DIR, 'log.log'),
                        level=logging.INFO)
    for handicap_elo, dynamic_factor in tqdm(EXPERIMENTS):
        run_with(handicap_elo, dynamic_factor)


if __name__ == '__main__':
    main()
