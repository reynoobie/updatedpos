er = 2
et = 2
adminUser = "admin"
adminPass = 1234

cashierUser = "cashier"
cashierPass = 1234

products = []
cart = []
while er == 2:  
    et = 2
    user = input("Enter User: ")
    password = int(input("Enter Password: "))
    if user == adminUser and password == adminPass:
        while et == 2:
            print("====================")
            print("        ADMIN       ")
            print("====================")
            print("1. View Products")
            print("2. Add Product")
            print("3. Change Product Price")
            print("4. Exit")
            choose = int(input("Choose: "))
            if choose == 1:
                s = 1
                print("====================")
                print("      PRODUCTS      ")
                print("====================")
                for i in products:
                    print(s,".", i)
                    s += 1
            elif choose == 2:
                prodAdd = input("Enter Product: ")
                products.append(prodAdd)
                print(prodAdd, "has been Added!")
            elif choose == 3:
                print("On dev")
            elif choose == 4:
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
        while et == 2: 
            print("====================")
            print("       CASHIER      ")
            print("====================")
            print("1. Add Item to Cart")
            print("2. View/Checkout")
            print("3. Logout")
            choose = int(input("Choose: "))
            if choose == 1:
                print("====================")
                print("      PRODUCTS      ")
                print("====================")
                for i in products:
                    print(i)
                addCart = input("Please Choose: ")
                if addCart in products:
                    cart.append(addCart)
                    print(addCart, "has been added to your Cart!")
                else:
                    print(addCart,"is not in Products")
            elif choose == 2:
                if len(cart) >= 1:
                    print("===== CART ====")
                    for i in cart:
                        print(i)
                    print("1. Checkout")
                    print("2. Back to the ball game")
                    cartchoose = int(input("Please Choose: "))
                    if cartchoose == 1:
                        print("Receipt is Printing...")
                        cart.clear()
                    elif cartchoose == 2:
                        print()
                    else:
                        print("Invalid Input")
                else:
                    print("No items in Cart Yet!") 
            elif choose == 3:
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
