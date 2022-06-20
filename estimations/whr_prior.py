from whr import whole_history_rating as whr
from whr.playerday import PlayerDay
from math import log, sqrt


def natural_rating2_to_elo2(nr):
    return nr * ((400 / log(10))**2)


base = whr.Base()
player = base.player_by_name('name')

# Fuente: https://github.com/pfmonville/whole_history_rating/blob/master/whr/player.py#L194
# Hago lo mismo, pero sin agregar una partida
playerday = PlayerDay(player, 0)
playerday.is_first_day = True
playerday.set_gamma(1) # Gamma 1 es elo 0
player.days.append(playerday)

player.update_uncertainty()

prior = playerday

if __name__ == '__main__':
    print('Prior mean:', prior.elo)
    print('Prior variance:', natural_rating2_to_elo2(prior.uncertainty))
    print('Prior stddev:', sqrt(natural_rating2_to_elo2(prior.uncertainty)))
