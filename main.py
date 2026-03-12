# test_resume.py
import os
import json
from tools.resume import parse_resume

result = parse_resume("./resume.pdf")

if "error" in result:
    print("Error:", result["error"])
else:
    print("Name:", result["name"])
    print("Current role:", result["current_role"])
    print("Skills:", result["skills"])
    print("\nFull output:")
    print(json.dumps(result, indent=2))