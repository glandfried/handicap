import math
from scipy.stats import norm

b = {
    2: 1.13672,
    3: 1.18795,
    4: 1.22841,
    5: 1.27457,
    6: 1.31978,
    7: 1.35881,
    8: 1.39782,
    9: 1.43614
}


def likelihood(r_black, r_white, komi, handicap, winner):
    if handicap <= 1:
        d = 0.580 - 0.0757 * komi
        sigma_px = 1.0649 - 0.0021976 * komi + 0.00014984 * (komi**2)
    else:
        d = handicap - 0.0757 * komi
        sigma_px = -0.0035169 * komi + b[handicap]

    rd = r_white - r_black - d

    p_white_wins = math.erfc(-rd/(sigma_px * math.sqrt(2))) / 2.0

    return p_white_wins if winner == "W" else (1.0 - p_white_wins)


def evidence(mu_black, sigma_black, mu_white, sigma_white, komi, handicap, winner):
    # Las estimaciones de habilidad tienen un bache entre 1.0 y -1.0
    mu_black = mu_black - 1.0 if mu_black > 0.0 else mu_black + 1.0
    mu_white = mu_white - 1.0 if mu_white > 0.0 else mu_white + 1.0

    steps = 21
    assert(steps % 2 == 1)
    k_sigmas = 6  # Integramos hasta k_sigmas desvios
    ret = 0.0
    lower_bound = -steps//2
    upper_bound = lower_bound + steps
    gap1 = 2 * k_sigmas * sigma_black / float(steps)
    gap2 = 2 * k_sigmas * sigma_white / float(steps)
    total_p = 0.0
    for i in range(lower_bound, upper_bound):
        for j in range(lower_bound, upper_bound):
            nmu_black = mu_black + i * gap1
            nmu_white = mu_white + j * gap2
            p = norm.pdf(nmu_black, mu_black, sigma_black) * norm.pdf(nmu_white, mu_white, sigma_white)
            total_p += p
            ret += p * likelihood(nmu_black, nmu_white, komi, handicap, winner)
    assert(abs(total_p * gap1 * gap2 - 1.0) < 0.0001)  # La probabilidad total tiene que dar 1!
    return ret * gap1 * gap2
