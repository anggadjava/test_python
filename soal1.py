string = ""

x = int(input("Masukkan angka :"))
line = x

if x>100:
    print("Jangan melebihi 100")
else:
    while line >= 0:
        kol = line*2
        while kol > 0:
            string = string+" "
            kol = kol - 1
        
        kanan = 1
        while kanan < (x - (line-1)):
            
            string = string + " #"
            kanan = kanan + 1
            
        string = string + "\n"
        line = line - 1
        
    print(string)
