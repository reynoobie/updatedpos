import os

def clear():
    os.system("cls") 


products = {
    "A1": {
        "name": "Uniform",
        "sizes": {
            "S": 450,
            "M": 500,
            "L": 550,
        }
    },
    "A2": {
        "name": "PE Pants",
        "sizes": {
            "S": 350,
            "M": 350,
            "L": 400
        }
    },
    "A3": {
        "name": "ID Lace",
        "sizes": {
            "Stan": 50
        }
    }
}


er = 2
et = 2
adminUser = "admin"
adminPass = 1234

cashierUser = "cashier"
cashierPass = 1234
cart = []

while er == 2:
    et = 2
    clear()
    user = input("Enter User: ")
    password = int(input("Enter Password: "))

    if user == adminUser and password == adminPass:
        while et == 2:
            clear()
            print("====================")
            print("        ADMIN       ")
            print("====================")
            print("")
            print("1. View Products")
            print("2. Exit")
            print("")
            choose = int(input("Choose: "))

            if choose == 1:
                clear()
                print("====================")
                print("      PRODUCTS      ")
                print("====================")
                print("")
                s = 1
                for i in products:
                    print(s, ".", i)
                    s += 1
                print("")
                input("Press ENTER to continue...")

            elif choose == 2:
                clear()
                print("1. Back to login")
                print("2. Exit Program")
                print("")
                choose2 = int(input("Choose: "))
                if choose2 == 1:
                    et = 1
                elif choose2 == 2:
                    er = 1
                    et = 1
                else:
                    print("Invalid Input!")
                    input("Press ENTER to continue...")
            else:
                print("Invalid Input")
                print("")
                input("Press ENTER to continue...")

   
    elif user == cashierUser and password == cashierPass:

     while et == 2:
        clear()
        print("====================")
        print("       CASHIER      ")
        print("====================")
        print("1. Add Item to Cart")
        print("2. View/Checkout")
        print("3. Logout")
        print("")
        choose = int(input("Choose: "))

        if choose == 1:
            clear()
            print("-" * 65)
            print(f"| {'CODE':<4} | {'NAME':<10} | {'PRICES':<43} |")
            print("-" * 65)

            for code, item in products.items():
                size_list = []
                for size, price in item["sizes"].items():
                    size_list.append(f"{size}:${price:.2f}")

                options_str = "Size: " + ", ".join(size_list)
                print(f"| {code:<4} | {item['name']:<10} | {options_str} |")
                print("-" * 65)

            print("")
            addCart = input("Enter Product Code to buy (e.g., A1): ").strip().upper()

            if addCart in products:
                selected_product = products[addCart]
                valid_sizes = list(selected_product['sizes'].keys())

                print(f"Selected: {selected_product['name']}")
                print(f"Available sizes: {valid_sizes}")
                print("")
                addSize = input("Enter Size: ").strip().upper()

                if addSize in selected_product["sizes"]:
                    qty = int(input("Enter Quantity: "))
                    if qty <= 0:
                        print("Invalid quantity!")
                        print("")
                        input("Press Enter...")
                        continue

                    price = selected_product["sizes"][addSize]
                    cart.append({
                        "code": addCart,
                        "name": selected_product["name"],
                        "size": addSize,
                        "qty": qty,
                        "price": price,
                        "subtotal": price * qty
                    })

                    print(f"--> Added {qty}x {addSize} {selected_product['name']} to cart!")
                    input("Press Enter to continue...")

                else:
                    print("Invalid Size!")
                    print("")
                    input("Press Enter...")
            else:
                print("Invalid Product Code!")
                print("")
                input("Press Enter...")   
       
        elif choose == 2:
            clear()
        print("-" * 65)
        print(f"| {'YOUR SHOPPING CART':^61} |")
        print("-" * 65)

        if not cart:
            print("Your cart is empty.")
            print("")
            input("Press Enter to return...")
        else:
            print(f"| {'NAME':<15} | {'SIZE':<6} | {'QTY':<5} | {'PRICE':<10} | {'SUBTOTAL':<12} |")
            print("-" * 65)

            grand_total = 0
   
            for item in cart:
                print(f"| {item['name']:<15} | {item['size']:<6} | {item['qty']:<5} | ${item['price']:<9.2f} | ${item['subtotal']:<11.2f} |")
                grand_total += item['subtotal']

            print("-" * 65)
            print(f"| {'TOTAL AMOUNT:':<40} ${grand_total:<19.2f} |")
            print("-" * 65)
            print("")

            action = input("Press (P) to Pay or (Enter) to go back: ").strip().upper()

            if action == "P":
                clear()
                while True:
                    try:
                        cash_str = input(f"Total is ${grand_total:.2f}. Enter Cash Amount: ")
                        cash = float(cash_str)

                        if cash >= grand_total:
                            change = cash - grand_total
                            print("")
                            print("=" * 30)
                            print("     TRANSACTION SUCCESSFUL")
                            print("=" * 30)
                            print(f" Total Due:   ${grand_total:.2f}")
                            print(f" Cash Paid:   ${cash:.2f}")
                            print(f" Change:      ${change:.2f}")
                            print("=" * 30)
                                             
                            cart.clear() 
                        
                            input("Press Enter to print receipt...")
                            break
                        else:
                            print(f">> Insufficient funds! You need ${grand_total - cash:.2f} more.")
                
                    except ValueError:
                        print(">> Invalid input. Please enter a number.")


