# Reporte: Red Base vs. Red Profunda en Iris (NumPy y Keras)

---

## 1. Comportamiento al agregar capas extra
Agregar dos capas más empeoró el aprendizaje en lugar de mejorarlo. En NumPy, la red base (4x3x3) redujo su error de ~0.75 a menos de 0.10, mientras que la profunda (4x3x3x3x3) se quedó atorada en ~0.67 casi todo el entrenamiento y apenas al final bajó a ~0.42. En Keras pasó lo mismo: la red base bajó la pérdida de 0.23 a 0.15, pero la profunda se estancó en ~0.22.

---

## 2. Comparación entre la red base de NumPy y Keras
Ambas bajan el error, pero sus curvas son distintas por la implementación de cada una. En NumPy los pesos inician con un aleatorio simple (`np.random.rand - 0.5`) y el entrenamiento procesa dato por dato en orden fijo, lo que hace que el error empiece alto (~0.75) y caiga de golpe al principio. En cambio, Keras usa inicialización Glorot/Xavier y entrena por mini-batches (de 32 datos), por lo que empieza con menor pérdida (~0.23) y muestra un descenso mucho más suave y constante.

---

## 3. ¿Por qué la red profunda no funcionó en Iris?
Hacer la red más grande no sirvió por dos razones. Primero, por el desvanecimiento del gradiente: como la derivada de la sigmoide es pequeña (=< 0.25), al multiplicar tantas capas en el backpropagation el gradiente que llega a la primera capa es casi cero y sus pesos no cambian. Segundo, porque Iris es un dataset pequeño (150 datos) y sencillo; no requiere tantas capas, por lo que agregar sigmoides y MSE solo saturó la red y la dejó estancada.