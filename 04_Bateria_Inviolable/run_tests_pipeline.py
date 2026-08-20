import subprocess
import sys
import os
import json
from datetime import datetime

def run_pipeline():
    print("=====================================================================")
    print("GUANES HEALTH - PIPELINE DE AUTOMATIZACIÓN Y VERIFICACIÓN DE MODELOS")
    print(f"Fecha/Hora de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=====================================================================\n")

    # Rutas de búsqueda de artefactos
    artifacts_dir = "/workspace/artifacts"
    scratch_dir = "/workspace/scratch"
    test_script = os.path.join(artifacts_dir, "test_simulador_homeostasis.py")
    
    if not os.path.exists(test_script):
        # Intentar en scratch
        test_script = os.path.join(scratch_dir, "test_simulador_homeostasis.py")
        if not os.path.exists(test_script):
            print(f"[-] ERROR: No se encontró el script de pruebas en {test_script} ni en {artifacts_dir}")
            sys.exit(1)

    print(f"[*] Utilizando suite de pruebas en: {test_script}")
    print("[*] Ejecutando suite de pruebas unitarias...")
    
    # Configurar el entorno de Python para que busque módulos también en artifacts y scratch
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{artifacts_dir}:{scratch_dir}:{env.get('PYTHONPATH', '')}"
    
    # Ejecutar la suite de pruebas mediante unittest
    result = subprocess.run(
        [sys.executable, test_script],
        capture_output=True,
        text=True,
        env=env
    )
    
    success = (result.returncode == 0)
    
    print("\n------------------ DETALLE DE LA CORRIDA ------------------")
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    print("-----------------------------------------------------------")

    # Registro de bitácora histórico de verificación
    log_file = os.path.join(scratch_dir, "pipeline_execution.log")
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "exit_code": result.returncode,
        "status": "PASS" if success else "FAIL",
        "details": result.stderr.strip() if result.stderr else "Ejecución exitosa"
    }
    
    try:
        # Añadir al log histórico en formato JSON Lines
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        print(f"[+] Bitácora actualizada correctamente en scratch.")
    except Exception as e:
        print(f"[-] Advertencia: No se pudo escribir en el archivo de logs: {str(e)}")

    if success:
        print("\n[✔] VEREDICTO: PASADO. El modelo se comporta bajo los inmutables físicos definidos.")
        sys.exit(0)
    else:
        print("\n[✘] VEREDICTO: FALLADO. Se detectó una regresión en las restricciones homeostáticas.")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
