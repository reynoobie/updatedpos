import os
import json
import uuid
import datetime
import time

# ==========================
# TERMINAL COLORS
# ==========================
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"

# ==========================
# UTILITY FUNCTIONS
# ==========================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header(text):
    print(CYAN + "╔" + "═" * 60 + "╗")
    print(f"        {text.upper():^60}")
    print("╚" + "═" * 60 + "╝" + RESET)

def success(msg):
    print(f"{GREEN}✔ {msg}{RESET}")

def error(msg):
    print(f"{RED}✘ {msg}{RESET}")

def option(num, text):
    print(f"{YELLOW}{num}.{WHITE} {text}{RESET}")

# ==========================
# DATA
# ==========================
users = {
    "admin": "1234",
    "cashier": "1234"
}

products = [
    {"name": "ID Lace", "price": 75},
    {"name": "Logo", "price": 50},
    {"name": "Cartolina", "price": 20},
    {"name": "Bond Paper", "price": 1}
]

def load_transactions():
    data = []
    if not os.path.exists("transactions.json"):
        open("transactions.json", "w").close()
    with open("transactions.json", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data

def save_transaction(cart, total, method, cash, change):
    receipt_id = str(uuid.uuid4())
    trans = {
        "receipt_id": receipt_id,
        "datetime": str(datetime.datetime.now()),
        "items": cart,
        "total": total,
        "method": method,
        "cash": cash,
        "change": change
    }
    with open("transactions.json", "a") as f:
        f.write(json.dumps(trans) + "\n")
    success(f"Transaction saved! Receipt ID: {receipt_id}")

# ==========================
# LOGIN
# ==========================
def login():
    clear()
    header("Login Page")
    print(f"{YELLOW}ADMIN || CASHIER \nPassword: 1234 {RESET}\n")
    user = input("Username ▶ ").lower()
    password = input("Password ▶ ")
    if user in users and password == users[user]:
        success("Login successful!")
        time.sleep(1)
        return user
    else:
        error("Invalid username/password")
        input("Press Enter to try again...")
        return None

# ==========================
# ADMIN DASHBOARD
# ==========================
# ==========================
# ADMIN DASHBOARD (SINGLE-SCREEN VIEW)
# ==========================
def admin_dashboard():
    transactions = load_transactions()
    selected_detail = None
    
    # Use the same width constants for consistent layout
    BOX_WIDTH = 50 
    TOTAL_WIDTH = BOX_WIDTH * 2 + 3 
    MAX_TRANS_DISPLAY = 15 # Max number of transactions to list on screen

    while True:
        clear()
        header("Admin Dashboard")
        
        # --- TOP SPLIT ---
        print("┌" + "─" * BOX_WIDTH + "┬" + "─" * BOX_WIDTH + "┐")
        print("│ " + "TRANSACTION LIST".ljust(BOX_WIDTH - 2) + "│ " + "TRANSACTION DETAILS".ljust(BOX_WIDTH - 2) + "│")
        print("├" + "─" * BOX_WIDTH + "┼" + "─" * BOX_WIDTH + "┤")
        
        # Determine how many rows to print (up to MAX_TRANS_DISPLAY)
        rows_to_print = max(MAX_TRANS_DISPLAY, len(transactions) if transactions else 0)

        # Draw the main content rows
        for i in range(rows_to_print):
            left_text = ""
            right_text = ""
            
            # LEFT SIDE: Transaction List
            if transactions and i < len(transactions):
                t = transactions[i]
                # Format: Index. Receipt_ID (Total)
                list_line = f"{i+1}. {t['receipt_id'][-8:]} (₱{t['total']}) - {t['datetime'][:10]}"
                # Highlight the selected transaction
                if selected_detail and t['receipt_id'] == selected_detail['receipt_id']:
                    left_text = f"{MAGENTA}{list_line}{RESET}"
                else:
                    left_text = list_line
            
            # RIGHT SIDE: Selected Details
            if i == 0:
                if selected_detail:
                    right_text = f"Receipt ID: {selected_detail['receipt_id']}"
                else:
                    right_text = YELLOW + "Select a transaction (Option 1)" + RESET
            elif selected_detail and i == 1:
                right_text = f"Date: {selected_detail['datetime']}"
            elif selected_detail and i == 2:
                right_text = "--- Items ---"
            
            # Print items in the right panel
            if selected_detail and i >= 3:
                item_list = selected_detail["items"]
                item_idx = i - 3
                if item_idx < len(item_list):
                    item = item_list[item_idx]
                    right_text = f" - {item['name']} x{item['qty']} = ₱{item['total']}"
                elif item_idx == len(item_list):
                    right_text = "---------------------"
                elif item_idx == len(item_list) + 1:
                    right_text = f"Total: ₱{selected_detail['total']}"
                elif item_idx == len(item_list) + 2:
                    right_text = f"Payment: {selected_detail['method']}"
                elif item_idx == len(item_list) + 3:
                    right_text = f"Cash: ₱{selected_detail['cash']}  Change: ₱{selected_detail['change']}"


            print(f"│ {left_text.ljust(BOX_WIDTH + len(MAGENTA) + len(RESET) - 2) if MAGENTA in left_text else left_text.ljust(BOX_WIDTH - 2)}│ {right_text.ljust(BOX_WIDTH - 2)}│")

        # --- SEPARATOR BETWEEN CONTENT AND OPTIONS ---
        print("├" + "─" * TOTAL_WIDTH + "┤")
        
        # --- OPTIONS ROW ---
        option_line = f"1. Select Transaction Number (1-{len(transactions)}) | 2. Logout"
        print("│ " + option_line.ljust(TOTAL_WIDTH - 2) + "│")
        print("└" + "─" * TOTAL_WIDTH + "┘")
        
        # --- USER INPUT LOGIC ---
        choice = input("\nChoose option ▶ ").lower()
        
        if choice == "1":
            if not transactions:
                error("No transactions to select!")
                time.sleep(1)
                continue
                
            sel = input(f"Enter transaction number (1-{len(transactions)}) ▶ ")
            if sel.isdigit() and 1 <= int(sel) <= len(transactions):
                selected_detail = transactions[int(sel) - 1]
                success(f"Transaction {sel} loaded.")
            else:
                error("Invalid selection!")
            time.sleep(1)
            
        elif choice == "2":
            break
            
        else:
            error("Invalid input!")
            time.sleep(1)

# ==========================
# CASHIER DASHBOARD 
# ==========================
def cashier_dashboard():
    cart = []
    total = 0
    
    # Custom box widths remain the same
    BOX_WIDTH_LEFT = 60
    BOX_WIDTH_RIGHT = 40
    TOTAL_WIDTH = BOX_WIDTH_LEFT + BOX_WIDTH_RIGHT + 3  # 60 + 40 + 3 = 103
    MAX_ROWS_DISPLAY = 15 # Max number of rows for products/cart combined

    while True:
        clear()
        header("Cashier Dashboard")

        # --- TOP ROW (Headers) ---
        print("┌" + "─" * BOX_WIDTH_LEFT + "┬" + "─" * BOX_WIDTH_RIGHT + "┐")
        print("│ " + "AVAILABLE PRODUCTS".ljust(BOX_WIDTH_LEFT - 2) + "│ " + "OPTIONS".ljust(BOX_WIDTH_RIGHT - 2) + "│")
        print("├" + "─" * BOX_WIDTH_LEFT + "┼" + "─" * BOX_WIDTH_RIGHT + "┤")
        
        # Options list for the right panel
        opt_list = ["1. Add Item to Cart", "2. Checkout", "3. Logout", "4. Remove Item from Cart"]
        
        # Draw Product List and Options
        # Loop for products and options (the content rows)
        max_content_rows = max(len(products), len(opt_list))
        for i in range(max_content_rows):
            
            # LEFT SIDE: Product List
            left_text = ""
            if i < len(products):
                p = products[i]
                left_text = f"{i+1}. {p['name']} - ₱{p['price']}"

            # RIGHT SIDE: Options
            right_text = opt_list[i] if i < len(opt_list) else ""

            print(f"│ {left_text.ljust(BOX_WIDTH_LEFT - 2)}│ {right_text.ljust(BOX_WIDTH_RIGHT - 2)}│")

        # --- SEPARATOR BETWEEN TOP SECTION AND CART ---
        # This line closes the Products/Options section and opens the Cart section
        print("├" + "─" * TOTAL_WIDTH + "┤")
        
        # --- CART HEADER ---
        # Cart now uses the full width for its header
        print("│ " + f"CART (Total: ₱{total})".ljust(TOTAL_WIDTH - 2) + "│")
        print("├" + "─" * TOTAL_WIDTH + "┤")
        
        # Draw Cart Content
        if cart:
            for i in range(len(cart)):
                if i < MAX_ROWS_DISPLAY: # Limit display length
                    item = cart[i]
                    line = f"{i+1}. {item['name']} x{item['qty']} = ₱{item['total']}"
                    print("│ " + line.ljust(TOTAL_WIDTH - 2)[:TOTAL_WIDTH - 2] + "│")
            if len(cart) > MAX_ROWS_DISPLAY:
                print("│ " + f"...({len(cart) - MAX_ROWS_DISPLAY} more items)".ljust(TOTAL_WIDTH - 2) + "│")
        else:
            print("│ " + "Cart is empty.".ljust(TOTAL_WIDTH - 2) + "│")

        # --- BOTTOM LINE ---
        print("└" + "─" * TOTAL_WIDTH + "┘")
        
        # --- USER INPUT LOGIC ---
        # The instruction is now only in the input prompt, which is clearer
        choice = input(f"\n{YELLOW}Choose option (1-4) or Product Number (1-{len(products)}): {RESET}").lower()

        # 1. ADD ITEM (No product list print)
        if choice == "1":
            product_num = input("Enter Product Number to Add (B to cancel):  ").lower()
            if product_num == "b":
                continue

            if product_num.isdigit() and 1 <= int(product_num) <= len(products):
                product = products[int(product_num) - 1]
                qty_input = input(f"Quantity for {product['name']} ▶ ")

                if qty_input.isdigit() and int(qty_input) > 0:
                    qty = int(qty_input)
                    cost = round(qty * product["price"], 2)
                    cart.append({"name": product["name"], "qty": qty, "price": product["price"], "total": cost})
                    total = round(total + cost, 2)
                    success(f"Added {qty} x {product['name']} = ₱{cost}")
                else:
                    error("Invalid quantity!")
            else:
                error("Invalid product number!")
            time.sleep(1)

        # 2. CHECKOUT
        elif choice == "2":
            if not cart:
                error("Cart is empty!")
                time.sleep(1)
                continue

            method = input("Payment method (cash/card) ▶ ").lower()
            if method not in ["cash", "card"]:
                error("Invalid method!")
                time.sleep(1)
                continue

            if method == "cash":
                cash_input = input(f"Enter cash amount (Required: ₱{total}) ▶ ")
                if not cash_input.isdigit() or float(cash_input) < total: 
                    error("Insufficient cash!")
                    time.sleep(1)
                    continue
                cash = float(cash_input)
                change = round(cash - total, 2)
            else:
                cash = total
                change = 0

            save_transaction(cart, total, method, cash, change)

            print("\n" + CYAN + "=== RECEIPT ===" + RESET)
            for item in cart:
                print(f"{item['name']} x{item['qty']} = ₱{item['total']}")
            print(f"Total: ₱{total}")
            print(f"Payment: {method}  Cash: ₱{cash}  Change: ₱{change}")
            input("\nPress Enter to finish...")

            cart.clear()
            total = 0
            time.sleep(0.5)

        # 3. LOGOUT
        elif choice == "3":
            break

        # 4. REMOVE ITEM
        elif choice == "4":
            if not cart:
                error("Cart is empty. Nothing to remove.")
                time.sleep(1)
                continue

            item_num_input = input("Enter Cart Item Number to Remove (B to cancel) ▶ ").lower()
            if item_num_input == "b":
                continue

            if item_num_input.isdigit():
                item_idx = int(item_num_input) - 1
                if 0 <= item_idx < len(cart):
                    removed_item = cart.pop(item_idx)
                    total = round(total - removed_item['total'], 2)
                    success(f"Removed 1 item: {removed_item['name']} (was x{removed_item['qty']})")
                else:
                    error("Invalid item number in cart!")
            else:
                error("Invalid input.")
            time.sleep(1)


        elif choice.isdigit() and 1 <= int(choice) <= len(products):
            product = products[int(choice) - 1]
            qty_input = input(f"Quantity for {product['name']} ▶ ")

            if qty_input.isdigit() and int(qty_input) > 0:
                qty = int(qty_input)
                cost = round(qty * product["price"], 2)
                cart.append({"name": product["name"], "qty": qty, "price": product["price"], "total": cost})
                total = round(total + cost, 2)
                success(f"Added {qty} x {product['name']} = ₱{cost}")
            else:
                error("Invalid quantity!")
            time.sleep(1)

        else:
            error("Invalid input!")
            time.sleep(1)

# ==========================
# MAIN LOOP
# ==========================
while True:
    user = login()
    if user == "admin":
        admin_dashboard()
    elif user == "cashier":
        cashier_dashboard()
