path = "../archivos/tres_aislados/log_juntos_"

header = "intra,inter,player,mu,sigma\n"

with open("../archivos/tres_aislados/log_juntos.csv", 'w') as f:
    f.write(header)
    for intra in range(1,21):
        for inter in ['8','80']:
            intra = str(intra)
            with open(path+intra+'_'+inter+'.txt', 'r') as f_in:
                for line in f_in:
                    [player,mu,sigma] = line.split()
                    new_line = intra +','+ inter +','+ player +','+ mu +','+ sigma +'\n'
                    f.write(new_line)
