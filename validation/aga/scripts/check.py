# original_filename = "../archivos/aago_validation/raago.csv"
# my_filename = "../archivos/aago_validation/results_"

original_filename = "handicap/validation/aga/archivos/aago_validation/raago.csv"
my_filename = "handicap/validation/aga/archivos/aago_validation/results_"


with open(original_filename, 'r') as orig_estimations :
    orig_estimations.readline() #salteo el header
    for line in orig_estimations:
        [id,mu,sigma,event_id,player_id] = line.split(',')
        player_id = player_id[:-1]
        with open(my_filename + event_id + '.txt', 'r') as my_estimations :
            for line in my_estimations :
                [my_player_id, my_mu, my_sigma] = line.split()
                if (str(player_id) == str(my_player_id)):
                    if mu == my_mu and sigma == my_sigma :
                        print(id + ': Correcto')
                    else:
                        print(id + ': ERROR')
                        print('  Mu esperado: ' + mu)
                        print('  Mu obtenido: ' + my_mu)
                        print('  Sigma esperado: ' + sigma)
                        print('  Sigma obtenido: ' + my_sigma)
