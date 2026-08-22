import subprocess
import sys
import os
import json
from datetime import datetime


def run_pipeline():
    print("Guanes Health — pipeline de regresion del modelo")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    bateria_dir = os.path.dirname(os.path.abspath(__file__))
    motor_dir = os.path.abspath(os.path.join(bateria_dir, "..", "03_Motor_Oncologico"))
    log_file = os.path.join(bateria_dir, "pipeline_execution.log")

    suites = [
        "test_inmuno_utils.py",
        "test_divergencia_estatico_vs_placa.py",
        "test_simulador_homeostasis.py",
        "test_simulador_homeostasis_v2.py",
        "test_simulador_homeostasis_v3.py",
        "test_simulador_homeostasis_v5.py",
        "test_parche_restauracion.py",
        "test_barrido_estocastico_oxigeno.py",
        "test_simulador_hepatocito.py",
        "test_simulador_onco_hepatico.py",
        "test_simulador_onco_hepatico_v2.py",
        "test_simulador_onco_hepatico_v3.py",
        "test_cart_hcc_interaccion.py",
        "test_analisis_sensibilidad_local_cart.py",
    ]

    env = os.environ.copy()
    sep = os.pathsep
    env["PYTHONPATH"] = sep.join(
        [motor_dir, bateria_dir, env.get("PYTHONPATH", "")]
    )

    overall_ok = True
    results = []

    for name in suites:
        test_script = os.path.join(bateria_dir, name)
        if not os.path.exists(test_script):
            print(f"[-] OMITIDO (no existe): {name}")
            continue

        print(f"[*] Ejecutando: {name}")
        result = subprocess.run(
            [sys.executable, test_script],
            capture_output=True,
            text=True,
            env=env,
            cwd=bateria_dir,
        )
        ok = result.returncode == 0
        overall_ok = overall_ok and ok
        results.append(
            {
                "suite": name,
                "exit_code": result.returncode,
                "status": "PASS" if ok else "FAIL",
            }
        )

        print("\n------------------ DETALLE ------------------")
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip())
        print("---------------------------------------------")
        tag = "OK" if ok else "FAIL"
        print(f"[{tag}] {name}\n")

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "status": "PASS" if overall_ok else "FAIL",
        "suites": results,
    }
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        print(f"[+] Bitacora: {log_file}")
    except OSError as e:
        print(f"[-] Advertencia: no se pudo escribir el log: {e}")

    if overall_ok:
        print("\n[OK] Pipeline PASS: suites alineadas con salidas del modelo.")
        sys.exit(0)

    print("\n[FAIL] Pipeline FAIL: regresion en una o mas suites.")
    sys.exit(1)


if __name__ == "__main__":
    run_pipeline()
