path = "../../archivos/intercomunidades/"
out_filename = path+"results.csv"

with open(out_filename, 'w') as f_out:
	f_out.write("intras,inters,id,mu,sigma\n")
	for i in range(1,21):
		i = 5*i
		for j in [8, 40, 80]:
			f_in = path + "log_separados_3_" + str(i)+"_"+str(j)+ ".txt"
			with open(f_in, 'r') as f:
				j = (j*5)/4
				for line in f:
					[id, mu, sigma] = line.split()
					f_out.write(str(i)+","+str(j)+","+id+","+mu+","+sigma+'\n')
			    	