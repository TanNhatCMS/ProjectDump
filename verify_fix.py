from aggregator import aggregate_code
from constants import TEXT_EN
import os

# Create a dummy project structure
test_dir = "test_project"
os.makedirs(test_dir, exist_ok=True)
with open(os.path.join(test_dir, "test.py"), "w") as f:
    f.write("print('hello')\n" * 10)

success = aggregate_code(test_dir, TEXT_EN)
print(f"Success: {success}")

# Check output
if os.path.exists(os.path.join(test_dir, "project_codebase.md")):
    print("Output file created successfully.")
    with open(os.path.join(test_dir, "project_codebase.md"), "r") as f:
        print(f.read())
else:
    print("Output file NOT created.")
