import pyrosetta
import math
import random
import heapq 
#Inicializar Pyrosetta
pyrosetta.init()

#Cargar estructura y función de puntuación
pose = pyrosetta.pose_from_pdb("insulina.pdb")
scorefxn = pyrosetta.create_score_function("ref2015_cart")

print("\n------- INFORMACIÓN DE LA ESTRUCTURA INICIAL -------")
#Calcular cantidad de aminoacidos
residuos = int(pose.total_residue())
print(f"Cantidad de residuos: {residuos}")

#Calcular angulos de la cadena lateral
for res_num in range(1, pose.total_residue() + 1):
    for chi in range(1, pose.residue(res_num).nchi() + 1):
        chi += chi

#Calcular total de angulos        
ang = 2*(residuos - 1) + chi
print(f"Cantidad de angulos de torsión: {ang}, con {chi} angulos laterales")

energia_inicial = scorefxn(pose)
print(f"Energía conformacional inicial: {energia_inicial}")

# Estructura para guardar las 10 mejores poses (como max-heap invertido)
mejores_poses = []
mejor_pose = pose.clone()
mejor_energia = scorefxn(pose)
heapq.heappush(mejores_poses, (-mejor_energia, 0, mejor_pose.clone()))  

# Parámetros del recocido
temp_inicial = 1500
temp_final = 5
alfa = 0.98
iteraciones = 65000
salto = 180  

# Contador para desempates en el heap
contador = 1
temp = temp_inicial
rango = list(range(-salto, salto + 1, 1))

print("\n------- INICIO DE RECOCIDO -------")
while temp > temp_final:
    for _ in range(iteraciones):
        pose_nueva = pose.clone()
        
        # Modificar ángulos
        for res_num in range(1, pose.total_residue() + 1):
            if res_num > 1:
                pose_nueva.set_phi(res_num, pose.phi(res_num) + random.choice(rango))
            if res_num < pose.total_residue():
                pose_nueva.set_psi(res_num, pose.psi(res_num) + random.choice(rango))
            for chi in range(1, pose_nueva.residue(res_num).nchi() + 1):
                pose_nueva.set_chi(chi, res_num, pose.chi(chi, res_num) + random.choice(rango))
        
        energia_nueva = scorefxn(pose_nueva)
        deltaE = energia_nueva - scorefxn(pose)

        if deltaE < 0 or random.random() < math.exp(-deltaE / temp):
            pose = pose_nueva
            
            # Actualizar la mejor conformación global
            if energia_nueva < mejor_energia:
                mejor_pose = pose_nueva.clone()
                mejor_energia = energia_nueva
            
            # Agregar al heap de mejores poses
            if len(mejores_poses) < 10:
                heapq.heappush(mejores_poses, (-energia_nueva, contador, pose_nueva.clone()))
                contador += 1
            else:
                # Reemplazar la peor de las top 10 si es mejor
                if energia_nueva < -mejores_poses[0][0]:
                    heapq.heappop(mejores_poses)
                    heapq.heappush(mejores_poses, (-energia_nueva, contador, pose_nueva.clone()))
                    contador += 1
    # Enfriamiento
    temp *= alfa
    print(f"Temp: {temp:.1f} | Energía actual: {energia_nueva:.2f} | Mejor Energía: {mejor_energia:.2f}")

#Minimización final de las mejores poses
print("\n------- MINIMIZACIÓN LOCAL -------")
#Aplicar relajación a los átomos forzados con ajuste de angulos
relax = pyrosetta.rosetta.protocols.relax.FastRelax(scorefxn, 3)
mejores_finales = []

for i, (energia, _, pose) in enumerate(sorted(mejores_poses)):
    relax.apply(pose)
    energia_final = scorefxn(pose)
    mejores_finales.append((energia_final, pose))
    print(f"Pose {i+1}: Energía inicial {-energia:.2f} | Energía final {energia_final:.2f}")

# Seleccionar las 10 mejores después de minimización
mejores_finales.sort()
top10_final = [pose for (energia, pose) in mejores_finales[:10]]

# Guardar resultados
print("\n" + "-" * 50)
for i, pose in enumerate(top10_final):
    energia = scorefxn(pose)
    print(f"Top {i+1}: Energía {energia:.2f}")
    pyrosetta.dump_pdb(pose, f"insulina_top{i+1}.pdb")

print(f"\nMejor energía final: {scorefxn(top10_final[0]):.2f}")
print("-" * 50)