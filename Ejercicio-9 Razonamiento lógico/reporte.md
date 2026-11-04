# Reporte breve:

**¿Por qué `Becario(Ana)` sale en el encadenamiento hacia adelante de
`AccesoNoche(Ana)` y no en el de hacia atrás?** Hacia adelante se aplican
todas las reglas que coinciden con los hechos, por eso se usa `R_beca`.
Hacia atrás solo se buscan reglas necesarias para probar el acceso; ser
becario no es un requisito.

**¿Por qué hacia atrás prueba `R_miembro_est` al buscar `Miembro(Marta)`, si
Marta es profesora?** Las reglas se intentan en el orden de la base. Primero
se prueba si Marta es estudiante, pero ese hecho no existe. Entonces falla
`R_miembro_est` y se intenta `R_miembro_prof`, que sí coincide con
`Profesor(Marta)`.

**Si se añade el hecho `TieneCredencial(Luis)` y se vuelve a preguntar
`AccesoNoche(Luis)`, ¿qué átomos nuevos aparecen y la consulta queda
probada? Compruébalo con tu programa y escribe el resultado.** Al volver a
ejecutar el programa, aparecen en este orden: `Miembro(Ana)`,
`Miembro(Luis)`, `Miembro(Marta)`, `Becario(Ana)`, `Becario(Luis)`,
`AccesoNoche(Ana)`, `AccesoNoche(Luis)` y `AccesoNoche(Marta)`. Comparado
con la ejecución sin la credencial de Luis, los nuevos por ese hecho son
`Miembro(Luis)`, `Becario(Luis)` y `AccesoNoche(Luis)`.
