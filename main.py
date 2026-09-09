import subprocess
import sys
import time

print("=" * 50)
print("MOIL AI Production Forecast System")
print("=" * 50)

print("\n[1/3] Generating synthetic dataset...")
time.sleep(1)

subprocess.run([
    sys.executable,
    "mechler/datageneration.py"
])

print("Dataset generated successfully.")

print("\n[2/3] Training production prediction model...")
time.sleep(1)

subprocess.run([
    sys.executable,
    "mechler/train.py"
])

print("Model trained successfully.")

print("\n[3/3] Running prediction system...")
time.sleep(1)

subprocess.run([
    sys.executable,
    "mechler/predict.py"
])

print("\nAnalysis Complete.")