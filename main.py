from mcp.server.fastmcp import FastMCP
from typing import List

# In-memory mock database with 20 leave days to start
employee_leaves = {
    "E001": {"balance": 18, "history": ["2024-12-25", "2025-01-01"]},
    "E002": {"balance": 20, "history": []},
}

# Create MCP server
mcp = FastMCP("LeaveManager")


# ──────────────────────────────────────────
# TOOLS
# ──────────────────────────────────────────


@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Check how many leave days are left for the employee"""
    data = employee_leaves.get(employee_id)
    if data:
        return f"{employee_id} has {data['balance']} leave days remaining."
    return "Employee ID not found."


@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """
    Apply leave for specific dates (e.g., ["2025-04-17", "2025-05-01"])
    """
    if employee_id not in employee_leaves:
        return "Employee ID not found."

    requested_days = len(leave_dates)
    available_balance = employee_leaves[employee_id]["balance"]

    if available_balance < requested_days:
        return (
            f"Insufficient leave balance. You requested {requested_days} day(s) "
            f"but have only {available_balance}."
        )

    employee_leaves[employee_id]["balance"] -= requested_days
    employee_leaves[employee_id]["history"].extend(leave_dates)

    return (
        f"Leave applied for {requested_days} day(s). "
        f"Remaining balance: {employee_leaves[employee_id]['balance']}."
    )


@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """Get leave history for the employee"""
    data = employee_leaves.get(employee_id)
    if data:
        history = ", ".join(data["history"]) if data["history"] else "No leaves taken."
        return f"Leave history for {employee_id}: {history}"
    return "Employee ID not found."


# ──────────────────────────────────────────
# RESOURCES
# ──────────────────────────────────────────


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! How can I assist you with leave management today?"


# ──────────────────────────────────────────
# PROMPTS
# ──────────────────────────────────────────


@mcp.prompt()
def check_balance_prompt(employee_id: str) -> str:
    """Prompt to check leave balance for an employee"""
    return (
        f"Please check the leave balance for employee ID {employee_id} "
        f"and give a clear summary of how many days they have remaining."
    )


@mcp.prompt()
def apply_leave_prompt(employee_id: str, leave_dates: str) -> str:
    """
    Prompt to apply leave for an employee.
    leave_dates should be a comma-separated string e.g. '2025-04-17, 2025-05-01'
    """
    return (
        f"Apply leave for employee {employee_id} on the following dates: {leave_dates}. "
        f"Parse the dates as a list and call the apply_leave tool. "
        f"After applying, confirm how many days were deducted and show the remaining balance."
    )


@mcp.prompt()
def leave_summary_prompt(employee_id: str) -> str:
    """Prompt to get a full leave summary — balance + history"""
    return (
        f"Give me a complete leave summary for employee {employee_id}. "
        f"This should include: "
        f"1) Their current leave balance. "
        f"2) Their full leave history with all dates taken. "
        f"Present this in a clean, readable format."
    )


@mcp.prompt()
def plan_leave_prompt(employee_id: str, num_days: int) -> str:
    """Prompt to help an employee plan upcoming leave"""
    return (
        f"Employee {employee_id} wants to plan {num_days} day(s) of leave. "
        f"First check their current balance. If they have enough days, "
        f"ask them which specific dates they'd like to take off. "
        f"If they don't have enough balance, inform them and suggest how many days they can take."
    )


@mcp.prompt()
def onboard_employee_prompt(employee_id: str) -> str:
    """Prompt to onboard a new employee into the leave system"""
    return (
        f"A new employee with ID {employee_id} is joining. "
        f"Check if they already exist in the system. "
        f"If not, greet them and explain: "
        f"1) They start with 20 leave days. "
        f"2) How to check their balance. "
        f"3) How to apply for leave by providing specific dates. "
        f"4) How to view their leave history."
    )


if __name__ == "__main__":
    mcp.run()
