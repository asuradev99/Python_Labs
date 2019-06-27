
with open ("Test.txt", "w+") as f:
    f.write("ashdkasj")
    f.seek(0)
    print(f.read())

