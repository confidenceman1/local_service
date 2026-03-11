import subprocess
import os

os.chdir("d:/Code/Data/local_service")

# 移除之前的远程仓库
subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)

# 添加正确的远程仓库
result = subprocess.run(
    ["git", "remote", "add", "origin", "https://github.com/confidenceman1/local_service.git"],
    capture_output=True,
    text=True
)
print("Add remote:", result.stderr if result.stderr else "OK")

# 推送代码
result = subprocess.run(
    ["git", "push", "-u", "origin", "master"],
    capture_output=True,
    text=True
)
print("Push result:")
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
