# Reporte sobre el desempeño de la red base vs. red profunda en Iris (NumPy y Keras)

---

## 1. ¿Qué pasó al agregar las dos capas extra?

En lugar de mejorar la precisión o bajar más rápido el error, agregar dos capas más empeoró bastante el aprendizaje en ambos notebooks.

* **En NumPy:** La red sencilla (4x3x3) fue reduciendo su error poco a poco desde casi 0.75 hasta llegar por debajo de 0.10 al terminar las 500 épocas. En cambio, la red profunda (4x3x3x3x3) se quedó prácticamente atorada con un error alto (alrededor de 0.67) durante las primeras 400 épocas, y apenas al final empezó a bajar un poco (llegando a ~0.42).
* **En Keras:** Pasó algo muy similar. El modelo base bajó su pérdida de 0.23 a 0.15 de forma constante, mientras que el modelo profundo apenas si se movió y se quedó atascado cerca de 0.22.

---

## 2. Comparación entre la red base de NumPy y la de Keras

Las dos redes terminan bajando el error, pero las gráficas no son iguales por cómo están programadas por dentro:

1. **Cómo inician los pesos:** En NumPy los pesos se inicializaron de forma aleatoria simple con `np.random.rand - 0.5`. Keras usa por defecto la inicialización de Glorot/Xavier, que ajusta mejor los valores iniciales para que la red no empiece tan a ciegas.
2. **El manejo de los datos:** En NumPy el entrenamiento va muestra por muestra (uno por uno en el orden en que viene el dataset). Keras junta los datos en pequeños grupos (batches de 32), lo que hace que la gráfica de pérdida sea mucho más suave y recta desde el inicio.
3. **Punto de partida:** Por estas mismas diferencias, la curva de NumPy empieza con un error más alto (casi 0.75) y cae rápido al principio, mientras que en Keras empieza más abajo (0.23) y baja de forma lineal.

---

## 3. ¿Por qué una red más profunda no funcionó mejor en Iris?

Hacer la red más grande no ayudó debido a dos razones principales:

* **Desvanecimiento del gradiente:** Al usar la función sigmoide, su derivada siempre entrega valores muy pequeños (máximo 0.25). Cuando la red tiene muchas capas, el algoritmo de backpropagation tiene que multiplicar esos valores pequeños una y otra vez para ajustar las primeras capas. Al final, el número que llega a la primera capa es prácticamente cero, por lo que sus pesos casi no cambian y la red no aprende.
* **El problema es sencillo:** El dataset Iris solo tiene 150 datos y 4 datos de entrada. No hace falta una red compleja para clasificarlo; con la red base de una sola capa oculta es más que suficiente. Meterle más capas con sigmoide y MSE solo provocó que la red se "saturara" y se quedara estancada.