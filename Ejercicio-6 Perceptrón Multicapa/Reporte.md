# Reporte sobre el desempeño de la red base vs. red profunda en Iris (NumPy y Keras)

---

## 1. ¿Qué pasó al agregar las dos capas extra?

En lugar de mejorar la precisión o bajar más rápido el error, agregar dos capas más empeoró bastante el aprendizaje en ambos notebooks.

* **En NumPy:** La red sencilla (4x3x3) fue reduciendo su error poco a poco desde casi 0.75 hasta llegar por debajo de 0.10 al terminar las 500 épocas. En cambio, la red profunda (4x3x3x3x3) se quedó prácticamente atorada con un error alto (alrededor de 0.67) durante las primeras 400 épocas, y apenas al final empezó a bajar un poco (llegando a ~0.42).
* **En Keras:** Pasó algo muy similar. El modelo base bajó su pérdida de 0.23 a 0.15 de forma constante, mientras que el modelo profundo apenas si se movió y se quedó atascado cerca de 0.22.

---

## 2. Comparación entre la red base de NumPy y la de Keras

Aunque las dos redes logran reducir el error conforme pasan las épocas, las gráficas muestran formas diferentes debido a cómo está implementado cada código por dentro. En primer lugar, la manera de inicializar los pesos cambia bastante: en NumPy los pesos se generan de forma aleatoria simple con `np.random.rand - 0.5`, mientras que Keras utiliza por defecto la inicialización de Glorot/Xavier, la cual escala mucho mejor los valores iniciales para evitar que la red empiece tan a ciegas. 

Por otro lado, la forma de procesar los datos durante el entrenamiento no es la misma. En el script de NumPy el aprendizaje se hace muestra por muestra en el orden exacto en que vienen los datos en el conjunto Iris, mientras que en Keras el optimizador agrupa la información en mini-batches (de 32 muestras por defecto), lo que ayuda a que el descenso de gradiente sea más estable y la gráfica de pérdida se vea mucho más suave desde las primeras épocas. 

Debido a estas diferencias de fondo, la curva de NumPy arranca con un error inicial considerablemente más alto (casi 0.75) y tiene una caída bastante marcada durante las primeras 100 épocas antes de aplanarse, mientras que en Keras la pérdida comienza desde un valor menor (~0.23) y va disminuyendo de forma casi lineal y constante durante todo el entrenamiento.

---

## 3. ¿Por qué una red más profunda no funcionó mejor en Iris?

Hacer la red más grande no ayudó debido a dos razones principales:

* **Desvanecimiento del gradiente:** Al usar la función sigmoide, su derivada siempre entrega valores muy pequeños (máximo 0.25). Cuando la red tiene muchas capas, el algoritmo de backpropagation tiene que multiplicar esos valores pequeños una y otra vez para ajustar las primeras capas. Al final, el número que llega a la primera capa es prácticamente cero, por lo que sus pesos casi no cambian y la red no aprende.
* **El problema es sencillo:** El dataset Iris solo tiene 150 datos y 4 datos de entrada. No hace falta una red compleja para clasificarlo; con la red base de una sola capa oculta es más que suficiente. Meterle más capas con sigmoide y MSE solo provocó que la red se "saturara" y se quedara estancada.