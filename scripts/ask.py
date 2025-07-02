import requests
import sys

API_URL = "http://localhost:8000/query"


def main() -> None:
    print("✱ LLM-MCP CLI  (exit: Ctrl-C / quit / exit)")
    while True:
        try:
            q = input("🟢 > ").strip()
            if q.lower() in ("exit", "quit"):
                break
            if not q:
                continue

            resp = requests.post(
                API_URL,
                json={"query": q},
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
            print("🟡", data["response"])
        except KeyboardInterrupt:
            break
        except requests.HTTPError as e:
            print("🔴 HTTP error:", e, file=sys.stderr)
        except Exception as exc:
            print("🔴", exc, file=sys.stderr)


if __name__ == "__main__":
    main()
