path = "../archivos/tres_aislados/log_separados_"

header = "file,intra,inter,intra2,player,mu,sigma\n"
file, intra, inter, intra2 = 'NULL','NULL','NULL','NULL'

with open("../archivos/tres_aislados/log_separados.csv", 'w') as f:
    f.write(header)
    file = '3'
    for intra in range(1,20):
        for inter in ['8','80']:
            top = 20-int(intra)
            for intra2 in range(top+1):
                intra = str(intra)
                intra2 = str(intra2)
                with open(path+file+'_'+intra+'_'+inter+'_'+intra2+'.txt', 'r') as f_in:
                    for line in f_in:
                        [player,mu,sigma] = line.split()
                        new_line = file +','+ intra +','+ inter +','+ intra2 +','+ player +','+ mu +','+ sigma +'\n'
                        f.write(new_line)

"""
    file = '1'
    for intra in range(1,20):
        intra = str(intra)
        with open(path+file+'_'+intra+'.txt', 'r') as f_in:
            for line in f_in:
                [player,mu,sigma] = line.split()
                new_line = file +','+ intra +','+ inter +','+ intra2 +','+ player +','+ mu +','+ sigma
                f.write(new_line)

    file = '2'
    for intra in range(1,20):
        intra = str(intra)
        for inter in ['8','80']:
            with open(path+file+'_'+intra+'_'+inter+'.txt', 'r') as f_in:
                for line in f_in:
                    [player,mu,sigma] = line.split()
                    new_line = file +','+ intra +','+ inter +','+ intra2 +','+ player +','+ mu +','+ sigma
                    f.write(new_line)
"""
