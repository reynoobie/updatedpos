import os
import uuid

def TransactionID():
    receiptID = str(uuid.uuid4())
    print("Transanction has been saved in", receiptID)

def clear():
    os.system("cls")
er = 2
et = 2
adminUser = "admin"
adminPass = "1234"

cashierUser = "cashier"
cashierPass = "1234"

products = [
    {"name": "ID Lace", "price": 75},
    {"name": "Logo", "price": 50},
    {"name": "Cartolina", "price": 20},
    {"name": "Bond Paper", "price": 1}
]
while er == 2:  
    et = 2
    user = input("Enter User: ")
    password = input("Enter Password: ")
    if user == adminUser and password == adminPass:
        clear()
        while et == 2:
            print("====================")
            print("        ADMIN       ")
            print("====================")
            print("1. View Transaction History")
            print("2. Exit")

            choose = int(input("Choose: "))

            if choose == 1:
                print("")

            elif choose == 2:
                print("1. Back to login")
                print("2. Exit Program")
                choose2 = int(input("Choose: "))   
                if choose2 == 1:
                    et = 1  
                elif choose2 == 2:
                    er = 1  
                    et = 1  
                else:
                    print("Invalid Input!")
            else:
                print("Invalid Input")

    

    elif user == cashierUser and password == cashierPass:
        clear()
        while et == 2: 
            print("====================")
            print("       CASHIER      ")
            print("====================")
            print("1. Add Item to Cart")
            print("2. Logout")
            choose = int(input("Choose: "))
            if choose == 1:
                clear()
                cart = []
                total = 0
                print("====================")
                print("      PRODUCTS      ")
                print("====================")
                print("Type \"Done\" if you're Finish or \"cancel\" to Clear Cart or \"view\" to View Cart")
                for i in products:
                    print(i['name'], "-  ₱", i['price'])
                while True:
                    item = input("Choose product: ")
                    if item.lower() == "view":
                        print("===== CART =====")
                        for i in cart:
                            print(i['name'], "x", i['qty'], "- ₱", i['total'], )
                        print("=================")
                    if item.lower() == "done":
                        break
                    if item.lower() == "cancel":
                        cart.clear()
                        total = 0
                        clear()
                        print("Cart has been Cleared!")
                        for i in products:
                            print(i['name'], "-  ₱", i['price'])
                        continue
                    for i in products:
                        if i["name"].lower() == item.lower():
                            qty = input("Quantity: ")
                            if not qty.isdigit():
                                print("Invalid Quanity!")
                                continue
                            qty = int(qty)
                            cost = i["price"] * qty
                            cart.append({
                                "name": i["name"],
                                "price": i["price"],
                                "qty": qty,
                                "total": cost
                            })
                            total += cost
                            if i["name"].lower() == item.lower():
                                print(f"Added {qty} x {i['name']} = ₱{cost}")
                            else:
                                print("There's no such product")
                clear()
                print("\n===== RECEIPT =====")
                for c in cart:
                    print(f"{c['name']} x{c['qty']} - ₱{c['total']}")
                print("-------------------")
                print(f"TOTAL: ₱{total}")
                print("===================")
                TransactionID()
                    
            elif choose == 2:
                clear()
                print("1. Back to login")
                print("2. Exit Program")
                choose2 = int(input("Choose: "))   
                if choose2 == 1:
                    et = 1  
                elif choose2 == 2:
                    er = 1  
                    et = 1  
                else:
                    print("Invalid Input!")
            else:
                print("Invalid Input!")
    else:
        print("Invalid User or Password!")