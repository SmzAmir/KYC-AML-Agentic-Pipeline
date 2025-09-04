# Minimal CLI with only stdlib deps
import argparse, json
from src.pipeline import healthcheck, example_task

def main():
    parser = argparse.ArgumentParser(description="Project CLI")
    parser.add_argument("--sum", nargs="*", type=float, default=[], help="Numbers to sum")
    args = parser.parse_args()
    payload = {f"x{i}": v for i, v in enumerate(args.sum)}
    result = example_task(payload)
    print(json.dumps({"health": healthcheck(), "result": result}))

if __name__ == "__main__":
    main()
