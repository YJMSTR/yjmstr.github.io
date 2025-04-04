#!/usr/bin/env python3
"""Minimal static dev server so `npm run dev` works for this static site.

Kimi Work preview may pass --host/--port (or set HOST/PORT env); a bare
positional port is also accepted, mirroring `python3 -m http.server`.
Stdlib only — works with any Python 3.
"""
import argparse
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "7100")))
    parser.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"))
    parser.add_argument("positional_port", nargs="?", type=int, default=None)
    args, _unknown = parser.parse_known_args()

    port = args.positional_port or args.port
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"Serving {os.getcwd()} at http://{args.host}:{port}", flush=True)
    server = ThreadingHTTPServer((args.host, port), SimpleHTTPRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
