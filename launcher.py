"""Desktop launcher: starts Streamlit locally and opens it in the browser."""
import os, socket, threading, webbrowser
from pathlib import Path
import streamlit.web.cli as stcli

def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

if __name__ == "__main__":
    app = Path(__file__).resolve().parent / "silver_analyzer.py"
    port = free_port()
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    threading.Timer(2, lambda: webbrowser.open(f"http://127.0.0.1:{port}")).start()
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    import sys
    sys.argv = ["streamlit", "run", str(app), "--server.address=127.0.0.1", f"--server.port={port}", "--server.headless=true", "--browser.gatherUsageStats=false"]
    stcli.main()
