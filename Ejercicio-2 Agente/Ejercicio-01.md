# Diagrama de la cueva, indicando agente, Wumpus, pits y oro.
![](https://github.com/OmarHerreraEspinosa/Curso-de-IA-LIC/blob/main/Agentes/Ejercicio-01/Mi%20Cueva%204x4.webp)

# Breve reporte.
- ¿Qué agentes lograron salir con el oro en tu mapa y cuáles no?
  El único agente que completó la misión con éxito fue el agente de aprendizaje, obteniendo el oro y escalando para salir de la cueva en 16 pasos con una puntuación de +984.
- ¿Por qué el agente de reflejo simple falla (o tiene suerte) en tu diseño?
  Falla porque no tiene memoria ni planificación. No sabe como reaccionar ni interpretar lo que está percibiendo, por eso al percibir el stench se queda dando vueltas hasta acabarse los 200 pasos, ya que no tiene una ruta trazada hacia el oro.
- ¿Cómo cambia el resultado del agente basado en modelo si acercas o alejas un pit de la casilla inicial?
  El agente funciona mejor cuando los pits están cerca porque los detecta rápido y los esquiva. Si los pits están lejos tiene más espacio para moverse, pero igual termina topándose con el Wumpus, cuando siente el stench y no encuentra otra ruta se queda trabado sin poder avanzar hacia el oro.
  
# Evidencias de haber corrido los 4 agentes con la nueva configuración del mundo.
# 02_simple_reflex_agent.py
![](https://github.com/OmarHerreraEspinosa/Curso-de-IA-LIC/blob/main/Agentes/Ejercicio-01/02_simple_reflex_agent.png)
# 03_model_based_agent.py
![](https://github.com/OmarHerreraEspinosa/Curso-de-IA-LIC/blob/main/Agentes/Ejercicio-01/03_model_based_agent.png)
# 04_goal_based_agent.py
![](https://github.com/OmarHerreraEspinosa/Curso-de-IA-LIC/blob/main/Agentes/Ejercicio-01/04_goal_based_agent.png)
# 05_utility_based_agent.py
![](https://github.com/OmarHerreraEspinosa/Curso-de-IA-LIC/blob/main/Agentes/Ejercicio-01/05_utility_based_agent.png)
# 06_learning_agent.py
![](https://github.com/OmarHerreraEspinosa/Curso-de-IA-LIC/blob/main/Agentes/Ejercicio-01/06_learning_agent.png)
