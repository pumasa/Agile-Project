import json

with open('./spork/database/user.json', 'r') as user:
    usr = json.loads(user.read())

    t = "test"    
    t1 = "test1"
    t2 = "test2"    
    for u in usr:
        print(u)
        print(u["userID"])
        print(u["email"])
        print(u["password"])
        if t == u["email"] or t == u["password"]:
            print("works")
        else:
            print("error")
        