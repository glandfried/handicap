import matplotlib.pyplot as plt

#plt.rcParams.update({'font.size': 15})
#fig, ax = plt.subplots()
#fig.set_figheight(7)
#fig.set_figwidth(8)
#bars = ax.bar(["AGA","WHR","TTT"], height = [0.41,0.54,0.58], width=0.5, align='center')
#ax.bar_label(bars)


def add_value_label(x_list,y_list):
    for i in range(0, len(x_list)):
        plt.text(i,y_list[i],y_list[i])

evidencias=[0.41,0.54,0.58]
estimadores=["AGA","WHR","TTT"]
plt.bar(estimadores,evidencias)
add_value_label(estimadores,evidencias)
#plt.title("Evidencia de los modelos")
plt.xlabel("Estimador")
plt.ylabel("Promedio geométrico de la evidencia")
plt.show()

plt.savefig('evidences_bar.png')
