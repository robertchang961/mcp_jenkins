"""Create a MCP server, register tools, and run MCP server."""

import logging
import pathlib
from datetime import date

from mcp.server.fastmcp import FastMCP

from prompts.register_prompts import register_prompts
from tools.register_tools import register_tools

pathlib.Path("logs").mkdir(parents=True, exist_ok=True)
today_date = date.today().strftime("%Y%m%d")
log_filepath = pathlib.Path(f"logs/mcp_jenkins_{today_date}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            filename=log_filepath,
            mode="a",
            encoding="utf-8",
        ),
    ],
    encoding="utf-8",
)


def main() -> None:
    """Create a MCP server, register tools, and run MCP server."""
    mcp = FastMCP(name="mcp_jenkins", port=8000)
    register_prompts(mcp)
    register_tools(mcp)
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
