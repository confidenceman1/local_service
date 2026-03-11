import subprocess
import os

os.chdir("d:/Code/Data/local_service")

# Add files
subprocess.run(["git", "add", "."], capture_output=True)

# Commit
result = subprocess.run(
    ["git", "commit", "-m", "Initial commit: local service AI prototype with AI script generator, marketing copy, and food recommender"],
    capture_output=True,
    text=True
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
