import sys

# Lista de paquetes críticos para el curso
packages = [
    "numpy",
    "matplotlib",
    "cosmoprimo",
    "classy",
    "pypower",
    "desilike",
    "cobaya",
    "jax",
    "camb"
]

print("--- Verifying ---")
failed = []

for pkg in packages:
    try:
        __import__(pkg)
        print(f"{pkg:15}: OK")
    except ImportError:
        print(f"{pkg:15}: FAIL")
        failed.append(pkg)

# Prueba de calculo real en CLASS (verifica GSL y OpenMP)
print("\n--- Testing CLASS ---")
try:
    from classy import Class
    cosmo = Class()
    cosmo.set({'h': 0.67, 'Omega_b': 0.022, 'Omega_cdm': 0.12})
    cosmo.compute()
    print("Result: OK")
except Exception as e:
    print(f"Result: FAIL ({e})")
    failed.append("classy_functional")

if not failed:
    print("Enviroment correctly installed.")
else:
    print(f"Troubles with: {', '.join(failed)}")
    sys.exit(1)
