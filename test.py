randomdict = {f"key{i}": f"value{i}" for i in range(10000)}

for i in range(10000):
    randomdict.pop(f"key{i}")
    
print(randomdict)