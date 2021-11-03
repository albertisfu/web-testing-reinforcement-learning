



def recursive(val, total):
    for i in range(5):
        for y in range(3):
            total = total  + i*y
    
    return total

total = 0
#total2 = recursive(1, total)
#print(total2)





def recursive2(val, numr):
    counter = 0
    for j in ['a','b','c', 'd']:
        counter = counter +1
        print('- contador recu y counter', numr, counter)
        print('j: ', j)
        if val != 0:
            print('val antes: ', val)
            val = val -1
            print('--call recursion--')
            numr = numr +1
            print('val des: ', val)
            recursive2(val, numr)
        
    
recursive2(2, 0)

