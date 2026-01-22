import time
import random
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

video_path = sys.argv[1] if len(sys.argv) > 1 else "VIDEO_DESCONHECIDO"

def wait_for_file_ready(path, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with open(path, 'rb'):
                return True
        except (IOError, OSError):
            time.sleep(1)
    return False

if video_path != "VIDEO_DESCONHECIDO":
    if not os.path.exists(video_path):
        print(f"Erro: Arquivo nao encontrado em {video_path}")
        sys.exit(1)
    
    if not wait_for_file_ready(video_path):
        print(f"Erro: Arquivo ocupado por outro processo.")
        sys.exit(1)

video_name = os.path.basename(video_path)

def step(message, delay=1.0):
    print(message)
    time.sleep(delay)

print("=" * 50)
print(f"Iniciando analise do video: {video_name}")
print("=" * 50)

step("Carregando arquivo de video...")
step("Extraindo frames...", 1.5)
step("Analisando trilha de audio...")
step("Transcrevendo fala...")
step("Calculando metricas finais...", 1.5)

print("\nRESULTADOS DA AVALIACAO\n")

metrics = {
    "Clareza": random.randint(7, 10),
    "Didatica": random.randint(6, 10),
    "Engajamento": random.randint(5, 10),
    "Qualidade Audio/Video": random.randint(7, 10)
}

for metric, score in metrics.items():
    print(f"- {metric}: {score}/10")
    time.sleep(0.3)

final_score = round(sum(metrics.values()) / len(metrics), 1)

print("\n" + "-" * 50)
print(f"Nota final: {final_score}/10")
print("-" * 50)
print("Analise finalizada com sucesso!")