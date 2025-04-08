# Optimización en ángulos de torsión de aminoácidos para reducir la energía conformacional de una estructura proteica🧬
Este repositorio implementa un algoritmo de recocido simulado para optimizar la estructura 3D de proteínas, minimizando su energía conformacional mediante la perturbación controlada de ángulos de torsión (φ, ψ, χ). El método utiliza PyRosetta para evaluar energías y ajustar conformaciones, partiendo de un archivo PDB con ruido artificial y generando una estructura refinada más estable.
## Motivación:
Proyecto desarrollado como introducción a la bioinformática computacional, con potencial aplicación en futuras investigaciones o trabajos de tesis
##Resultados:
El algoritmo no sólo recuperó una estructura estable desde una conformación distorsionada, sino que alcanzó un mínimo energético más profundo que el de la estructura nativa original, bajo la métrica de la función ref2015_cart.
<table>
  <tr>
    <td align="center"><img src="img/p1.png" width="400"></td>
    <td align="center"><img src="img/p1_1.png" width="400"></td>
  </tr>
  <tr>
    <td align="center">Figura 1: Descripción imagen 1</td>
    <td align="center">Figura 2: Descripción imagen 2</td>
  </tr>
</table>
