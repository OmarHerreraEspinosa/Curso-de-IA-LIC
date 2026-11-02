# Reporte — Cliff Walking

El camino que va junto al acantilado es óptimo porque desde S se puede subir
una casilla, avanzar once veces a la derecha y bajar a G. Son 13 pasos, que
es la menor cantidad posible para llegar a la meta sin caer. Cada paso cuesta
−1, así que el retorno es −13. Si el agente da más pasos, recibe más
recompensas de −1; y si cae al acantilado, recibe −100. Por eso ese camino
corto y seguro es la mejor opción.

La curva de entrenamiento puede quedar por debajo de −13 aunque la política
voraz ya encuentre ese camino porque durante el entrenamiento el agente todavía
explora: con ε = 0.1, a veces elige una acción al azar. Puede alejarse de la
ruta o caer al acantilado, recibir −100 y tener que volver a empezar desde S.
Eso empeora la recompensa de ese episodio. En la evaluación, en cambio, no hay
exploración (ε = 0), así que el agente sigue la política aprendida sin elegir
acciones al azar.

Cuando el agente cae al acantilado, en la actualización de Q-learning el
estado siguiente `s'` es S, es decir, `(3, 0)`. La caída da −100, pero el
episodio no termina: el agente regresa a S y sigue jugando. Por eso S no es
un estado terminal y el objetivo de la actualización incluye el mejor valor
Q de las acciones desde S. Solo llegar a G termina el episodio; en ese caso,
el valor futuro sí es 0.
