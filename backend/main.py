"""
test_resume_prep.py — Test resume parsing and prep doc generation locally.
Run: python test_resume_prep.py resume.pdf
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tools.resume import parse_resume
from tools.prep import generate_prep_doc


def main():
    # Get resume path from command line or use default
    resume_path = sys.argv[1] if len(sys.argv) > 1 else "resume.pdf"

    print("=" * 50)
    print("STEP 1: Parsing resume...")
    print("=" * 50)

    profile = parse_resume(resume_path)

    if "error" in profile:
        print("Error:", profile["error"])
        sys.exit(1)

    print("Name:        ", profile.get("name"))
    print("Current role:", profile.get("current_role"))
    print("Skills:      ", profile.get("skills"))
    print("\nFull parsed output:")
    print(json.dumps(profile, indent=2))

    print("\n" + "=" * 50)
    print("STEP 2: Generating prep doc...")
    print("=" * 50)

    result = generate_prep_doc(
        person_name=profile.get("name", "Unknown"),
        profile_data=profile,
        meeting_context="Coffee chat to learn about their career path",
        your_background="Software engineer interested in learning from their experience",
    )

    if "error" in result:
        print("Error:", result["error"])
        sys.exit(1)

    print(result["document"])


if __name__ == "__main__":
    main()