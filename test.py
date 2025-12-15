from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
import os, uuid, json, datetime, sys

console = Console()

# ==========================
#  TERMINAL COLOR CODES
# ==========================
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def exit():
    sys.exit()

def header(text, color=CYAN):
    print(color + "╔══════════════════════════════════════════╗")
    print(f"                 {text.upper()}")
    print("╚══════════════════════════════════════════╝" + RESET)

# ==========================
# DATA HANDLING
# ==========================
TRANSACTION_FILE = "transactions.json"

def load_transactions():
    if not os.path.exists(TRANSACTION_FILE):
        open(TRANSACTION_FILE, "w").close()
    data = []
    with open(TRANSACTION_FILE, "r") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data

def save_transaction(items, total, method, cash, change):
    receipt_id = str(uuid.uuid4())
    trans = {
        "receipt_id": receipt_id,
        "datetime": str(datetime.datetime.now()),
        "items": items,
        "total": total,
        "method": method,
        "cash": cash,
        "change": change
    }
    with open(TRANSACTION_FILE, "a") as f:
        f.write(json.dumps(trans) + "\n")
    console.print(f"[green]Transaction saved! Receipt ID: {receipt_id}[/green]")

# ==========================
# PRODUCTS & USERS
# ==========================
PRODUCTS = [
    {"name": "ID Lace", "price": 75},
    {"name": "Logo", "price": 50},
    {"name": "Cartolina", "price": 20},
    {"name": "Bond Paper", "price": 1}
]

USERS = {"admin": "1234", "cashier": "1234"}

# ==========================
# PANEL BUILDERS
# ==========================
def build_dashboard_panel(user_name):
    return Panel(f"[bold green]Logged in as:[/bold green] {user_name}", title="Dashboard")

def build_products_panel():
    table = Table(title="Products")
    table.add_column("No.", justify="right")
    table.add_column("Name")
    table.add_column("Price", justify="right")

    for idx, p in enumerate(PRODUCTS, start=1):
        table.add_row(str(idx), p["name"], f"₱{p['price']}")

    return Panel(table, title="Products")

def build_cart_panel(cart):
    table = Table(title="Cart")
    table.add_column("Item")
    table.add_column("Qty", justify="right")
    table.add_column("Price", justify="right")
    table.add_column("Total", justify="right")

    total = 0
    for c in cart:
        table.add_row(
            c["name"],
            str(c["qty"]),
            f"₱{c['price']}",
            f"₱{c['total']}"
        )
        total += c["total"]

    table.add_row("", "", "[bold magenta]TOTAL[/bold magenta]", f"[white]₱{total}")
    return Panel(table, title="Cart")

def build_admin_top_panel(user_name):
    return Panel(f"[bold green]Logged in as:[/bold green] {user_name}", title="Dashboard")

def build_transaction_list_panel(transactions):
    table = Table(title="Transactions")
    table.add_column("No.", justify="right")
    table.add_column("Receipt ID")

    for idx, t in enumerate(transactions, start=1):
        table.add_row(str(idx), t["receipt_id"])

    return Panel(table, title="Transaction List")

def build_transaction_detail_panel(selected):
    if not selected:
        return Panel("No transaction selected", title="Transaction Details")

    lines = [
        f"[magenta]Receipt ID:[white] {selected['receipt_id']}",
        f"[magenta]Datetime:[white] {selected['datetime']}",
        "[magenta]Items:[white]"
    ]

    for item in selected["items"]:
        lines.append(
            f" [green]- {item['name']} x{item['qty']} = ₱{item['total']}"
        )

    lines.extend([
        f"[magenta]TOTAL:[white] ₱{selected['total']}",
        f"[magenta]Paid Using:[white] {selected['method']}",
        f"[magenta]Amount Paid:[white] ₱{selected['cash']}",
        f"[magenta]Change:[white] ₱{selected['change']}"
    ])

    return Panel("\n".join(lines), title="Transaction Details")

# ==========================
# LAYOUT SETUP
# ==========================
def create_cashier_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="top", size=3),
        Layout(name="bottom")
    )
    layout["bottom"].split_row(
        Layout(name="products"),
        Layout(name="cart")
    )
    return layout

def create_admin_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="top", size=3),
        Layout(name="bottom")
    )
    layout["bottom"].split_row(
        Layout(name="txn_list"),
        Layout(name="txn_detail")
    )
    return layout

# ==========================
# INTERFACES
# ==========================
def admin_interface(user_name="admin"):
    layout = create_admin_layout()
    transactions = load_transactions()
    selected_txn = None

    while True:
        clear()
        layout["top"].update(build_admin_top_panel(user_name))
        layout["txn_list"].update(build_transaction_list_panel(transactions))
        layout["txn_detail"].update(build_transaction_detail_panel(selected_txn))

        console.clear()
        console.print(layout)

        choice = Prompt.ask("Choose option ([green]1[/green] = View, [green]2[/green] = Back to login,[green]3[/green] = Exit program)")

        if choice == "1":
            if not transactions:
                Prompt.ask("No transactions. Press Enter")
                continue

            txn_no = Prompt.ask("Transaction number (or cancel)")
            if txn_no.lower() == "cancel":
                continue

            if txn_no.isdigit() and 1 <= int(txn_no) <= len(transactions):
                selected_txn = transactions[int(txn_no) - 1]
            else:
                Prompt.ask("Invalid selection. Press Enter")

        elif choice == "2":
            break
        elif choice == "3":
            clear()
            exit()

def cashier_interface(user_name="cashier"):
    cart = []
    layout = create_cashier_layout()

    while True:
        clear()
        layout["top"].update(build_dashboard_panel(user_name))
        layout["products"].update(build_products_panel())
        layout["cart"].update(build_cart_panel(cart))

        console.clear()
        console.print(layout)

        choice = Prompt.ask(
            "Select product [1-4] | [green]D[/green] = Finish | [green]C[/green] = Clear | [green]cancel[/green] = Exit"
        ).lower()

        if choice == "cancel":
            break

        elif choice == "c":
            cart.clear()

        elif choice == "d":
            if not cart:
                Prompt.ask("Cart empty. Press Enter")
                continue

            total = sum(c["total"] for c in cart)
            method = Prompt.ask("Payment Method", choices=["cash", "card"])

            if method == "cash":
                cash = IntPrompt.ask("Enter cash")
                if cash < total:
                    Prompt.ask("Insufficient cash. Press Enter")
                    continue
                change = cash - total
            else:
                cash = total
                change = 0

            clear()
            header("Receipt")

            for c in cart:
                print(f"{WHITE}{c['name']} x{c['qty']} - ₱{c['total']}")

            print("---------------------")
            print(f"{MAGENTA}TOTAL:{WHITE} ₱{total}")
            print(f"{MAGENTA}Payment:{WHITE} {method}")
            print(f"{MAGENTA}Paid:{WHITE} ₱{cash}")
            print(f"{MAGENTA}Change:{WHITE} ₱{change}")

            save_transaction(cart, total, method, cash, change)
            input("Press Enter...")
            cart.clear()

        else:
            if not choice.isdigit():
                continue

            index = int(choice) - 1
            if index < 0 or index >= len(PRODUCTS):
                continue

            product = PRODUCTS[index]
            qty = IntPrompt.ask(f"Quantity for {product['name']}")
            cart.append({
                "name": product["name"],
                "price": product["price"],
                "qty": qty,
                "total": product["price"] * qty
            })

# ==========================
# LOGIN
# ==========================
def login():
    while True:
        clear()
        console.clear()
        console.print(build_dashboard_panel("Please login (admin/cashier)"))

        user = Prompt.ask("User").lower()
        password = Prompt.ask("Password", password=True)

        if user in USERS and USERS[user] == password:
            if user == "admin":
                admin_interface(user)
            else:
                cashier_interface(user)
        else:
            Prompt.ask("Invalid login. Press Enter")

# ==========================
# MAIN
# ==========================
if __name__ == "__main__":
    login()
