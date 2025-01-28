import sys
import z3

equationParams = []

for line in sys.stdin:
    line = line.strip()
    equationParams.append(tuple(map(float, line.split(" "))))

px = z3.Real('px')
py = z3.Real('py')
pz = z3.Real('pz')
vx = z3.Real('vx')
vy = z3.Real('vy')
vz = z3.Real('vz')
solver = z3.Solver()

for i in range(len(equationParams)):
    px_i, py_i, pz_i, vx_i, vy_i, vz_i = equationParams[i]
    t_i = z3.Real(f"t_{i}")
    solver.add(px_i + vx_i * t_i == px + vx * t_i)
    solver.add(py_i + vy_i * t_i == py + vy * t_i)
    solver.add(pz_i + vz_i * t_i == pz + vz * t_i)

solver.check()
result = solver.model()
print(result[px], result[py], result[pz], result[vx], result[vy], result[vz])
