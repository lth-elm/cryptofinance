import numpy as np


def att_one_plus_two(cycle, hash_power_list):
    result_list = []
    theoretical_list = []

    for p in hash_power_list:
        q = 1 - p
        rendement_val = rendement(cycle, p)
        result_list.append(rendement_val)
        rendement_thq = (3*p**3 + 4*q*p**2) / (q + 3*p**3 + 4*q*p**2 + 2*q**2*p)
        theoretical_list.append(rendement_thq)
    
    return result_list, theoretical_list


def rendement(cycle, p):
    ER = 0
    EH = 0
    for _ in range(cycle):
        R, H = block_simulation(p)
        ER += R
        EH += H
    return ER/EH


def block_simulation(proba):
    block1 = np.random.choice(('A','B'), p=[proba, 1-proba])
    
    if (block1 =='A'): # A..
        block2 = np.random.choice(('A','B'), p=[proba, 1-proba])
        block3 = np.random.choice(('A','B'), p=[proba, 1-proba])
        
        if(block2 =='A'): # AA.
            
            if(block3 =='A'): # AAA
                return 3, 3
            else: # AAB
                return 2, 2
        
        else: # AB.
            
            if(block3 =='A'): # ABA
                return 2, 2     
            else: # ABB
                return 0, 2
        
    else: # B..
        return 0, 1





# n = 10000
# hash_power_list = np.arange(0.30,0.49,0.01)
# result_list, theoretical_list = att_one_plus_two(n, hash_power_list)


# fig, ax = plt.subplots()
# ax.plot(hash_power_list, hash_power_list, color='black')
# ax.plot(hash_power_list, result_list, color='blue')
# ax.plot(hash_power_list, theoretical_list, color='green')

# ax.set_xlabel("Hash Power")
# ax.set_ylabel("Profitability")

# plt.show()