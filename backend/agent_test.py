# main.py
import sys
sys.path.insert(0, ".")

from agent import prep_for_networking_call

def main():
    print("=" * 60)
    print("       Cappuccino AI — Networking Prep")
    print("=" * 60)

    company    = input("\nCompany name: ").strip()
    job_title  = input("Job title:    ").strip()
    background = input("Your background (press enter to skip): ").strip()

    if not company or not job_title:
        print("Company and job title are required.")
        sys.exit(1)

    result = prep_for_networking_call(company, job_title, background)
    print(result)

if __name__ == "__main__":
    main()