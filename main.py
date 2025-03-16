import os
import subprocess
from typing import List, Optional
from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP


# Environment variable for ledger file path with default
# First check command-line argument, then environment variable
LEDGER_FILE = os.getenv("LEDGER_FILE")

# Initialize MCP server
mcp = FastMCP("Ledger CLI")


# Pydantic models for ledger commands
class LedgerBalance(BaseModel):
    query: Optional[str] = Field(None, description="Filter accounts by regex pattern")
    begin_date: Optional[str] = Field(
        None, description="Start date for transactions (YYYY/MM/DD)"
    )
    end_date: Optional[str] = Field(
        None, description="End date for transactions (YYYY/MM/DD)"
    )
    depth: Optional[int] = Field(None, description="Limit account depth displayed")
    monthly: bool = Field(False, description="Group by month")
    weekly: bool = Field(False, description="Group by week")
    daily: bool = Field(False, description="Group by day")
    yearly: bool = Field(False, description="Group by year")
    flat: bool = Field(False, description="Show full account names without indentation")
    no_total: bool = Field(False, description="Don't show the final total")


class LedgerRegister(BaseModel):
    query: Optional[str] = Field(
        None, description="Filter transactions by regex pattern"
    )
    begin_date: Optional[str] = Field(
        None, description="Start date for transactions (YYYY/MM/DD)"
    )
    end_date: Optional[str] = Field(
        None, description="End date for transactions (YYYY/MM/DD)"
    )
    monthly: bool = Field(False, description="Group by month")
    weekly: bool = Field(False, description="Group by week")
    daily: bool = Field(False, description="Group by day")
    yearly: bool = Field(False, description="Group by year")
    sort: Optional[str] = Field(
        None, description="Sort transactions (date, amount, payee)"
    )
    by_payee: bool = Field(False, description="Group by payee")
    current: bool = Field(
        False, description="Show only transactions on or before today"
    )


class LedgerAccounts(BaseModel):
    query: Optional[str] = Field(None, description="Filter accounts by regex pattern")


class LedgerPayees(BaseModel):
    query: Optional[str] = Field(None, description="Filter payees by regex pattern")


class LedgerCommodities(BaseModel):
    query: Optional[str] = Field(
        None, description="Filter commodities by regex pattern"
    )


class LedgerPrint(BaseModel):
    query: Optional[str] = Field(
        None, description="Filter transactions by regex pattern"
    )
    begin_date: Optional[str] = Field(
        None, description="Start date for transactions (YYYY/MM/DD)"
    )
    end_date: Optional[str] = Field(
        None, description="End date for transactions (YYYY/MM/DD)"
    )


class LedgerStats(BaseModel):
    query: Optional[str] = Field(None, description="Filter for statistics")


class LedgerBudget(BaseModel):
    query: Optional[str] = Field(None, description="Filter accounts by regex pattern")
    begin_date: Optional[str] = Field(
        None, description="Start date for transactions (YYYY/MM/DD)"
    )
    end_date: Optional[str] = Field(
        None, description="End date for transactions (YYYY/MM/DD)"
    )
    monthly: bool = Field(False, description="Group by month")
    weekly: bool = Field(False, description="Group by week")
    daily: bool = Field(False, description="Group by day")
    yearly: bool = Field(False, description="Group by year")


class LedgerRawCommand(BaseModel):
    command: List[str] = Field(..., description="Raw ledger command arguments")


# Helper function to run ledger commands
def run_ledger(args: List[str]) -> str:
    try:
        if not LEDGER_FILE:
            return "Ledger file path not set. Please provide it via --ledger-file argument or LEDGER_FILE environment variable."

        # Validate inputs to prevent command injection
        for arg in args:
            if ";" in arg or "&" in arg or "|" in arg:
                return "Error: Invalid characters in command arguments."

        result = subprocess.run(
            ["ledger", "-f", LEDGER_FILE] + args,
            check=True,
            text=True,
            capture_output=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_message = f"Ledger command failed: {e.stderr}"
        if "couldn't find file" in e.stderr:
            error_message = f"Ledger file not found at {LEDGER_FILE}. Please provide a valid path via --ledger-file argument or LEDGER_FILE environment variable."
        return error_message


# Define MCP tools
@mcp.tool(description="Show account balances")
def ledger_balance(params: LedgerBalance) -> str:
    cmd = ["balance"]

    if params.query:
        cmd.append(params.query)
    if params.begin_date:
        cmd.extend(["-b", params.begin_date])
    if params.end_date:
        cmd.extend(["-e", params.end_date])
    if params.depth is not None:
        cmd.extend(["--depth", str(params.depth)])
    if params.monthly:
        cmd.append("--monthly")
    if params.weekly:
        cmd.append("--weekly")
    if params.daily:
        cmd.append("--daily")
    if params.yearly:
        cmd.append("--yearly")
    if params.flat:
        cmd.append("--flat")
    if params.no_total:
        cmd.append("--no-total")

    return run_ledger(cmd)


@mcp.tool(description="Show transaction register")
def ledger_register(params: LedgerRegister) -> str:
    cmd = ["register"]

    if params.query:
        cmd.append(params.query)
    if params.begin_date:
        cmd.extend(["-b", params.begin_date])
    if params.end_date:
        cmd.extend(["-e", params.end_date])
    if params.monthly:
        cmd.append("--monthly")
    if params.weekly:
        cmd.append("--weekly")
    if params.daily:
        cmd.append("--daily")
    if params.yearly:
        cmd.append("--yearly")
    if params.sort:
        cmd.extend(["-S", params.sort])
    if params.by_payee:
        cmd.append("-P")
    if params.current:
        cmd.append("-c")

    return run_ledger(cmd)


@mcp.tool(description="List all accounts")
def ledger_accounts(params: LedgerAccounts) -> str:
    cmd = ["accounts"]

    if params.query:
        cmd.append(params.query)

    return run_ledger(cmd)


@mcp.tool(description="List all payees")
def ledger_payees(params: LedgerPayees) -> str:
    cmd = ["payees"]

    if params.query:
        cmd.append(params.query)

    return run_ledger(cmd)


@mcp.tool(description="List all commodities")
def ledger_commodities(params: LedgerCommodities) -> str:
    cmd = ["commodities"]

    if params.query:
        cmd.append(params.query)

    return run_ledger(cmd)


@mcp.tool(description="Print transactions in ledger format")
def ledger_print(params: LedgerPrint) -> str:
    cmd = ["print"]

    if params.query:
        cmd.append(params.query)
    if params.begin_date:
        cmd.extend(["-b", params.begin_date])
    if params.end_date:
        cmd.extend(["-e", params.end_date])

    return run_ledger(cmd)


@mcp.tool(description="Show statistics about the ledger file")
def ledger_stats(params: LedgerStats) -> str:
    cmd = ["stats"]

    if params.query:
        cmd.append(params.query)

    return run_ledger(cmd)


@mcp.tool(description="Show budget report")
def ledger_budget(params: LedgerBudget) -> str:
    cmd = ["budget"]

    if params.query:
        cmd.append(params.query)
    if params.begin_date:
        cmd.extend(["-b", params.begin_date])
    if params.end_date:
        cmd.extend(["-e", params.end_date])
    if params.monthly:
        cmd.append("--monthly")
    if params.weekly:
        cmd.append("--weekly")
    if params.daily:
        cmd.append("--daily")
    if params.yearly:
        cmd.append("--yearly")

    return run_ledger(cmd)


@mcp.tool(description="Run a raw ledger command")
def ledger_raw_command(params: LedgerRawCommand) -> str:
    return run_ledger(params.command)


@mcp.resource("ledger://file")
def get_ledger_file() -> str:
    """Return the path to the current ledger file."""
    return LEDGER_FILE or ""
