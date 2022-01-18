import random
import numpy as np
import matplotlib.pyplot as plt


def double_spending(attempt, z, limit):
    hashrate_list = []
    probability_of_success = []


    for hashrate in np.arange(0, 0.49, 0.01):
        hashrate_list.append(hashrate)

        # SET CONSTANTS AND VARIABLES

        ATTEMPTS = attempt # attempts

        Z = z # confirmation
        LIMIT = limit # maximum interval limit between mainchain and secret chain

        successfull_attacks = 0

        for _ in range(ATTEMPTS):
            attacker_chain = 1 # Alice sends a transaction to herself registred in a secret block ... 
            mainchain = 1 # ... In parallel, she publicly sends this transaction to Bob

            while (mainchain - attacker_chain) < LIMIT: # difference between our secret chain and mainchain since the start of the attack 
                p = random.uniform(0, 1)

                if(p < hashrate): # attacker finds the next block secretely
                    attacker_chain += 1
                else:
                    mainchain +=1
                
                if attacker_chain > Z or mainchain > Z:
                    break

            if mainchain-attacker_chain >= LIMIT: # difference between us and mainchain to big to overtake so we give up on this attempt
                continue

            if attacker_chain > mainchain: # make all secret blocks public and force the network to accept these blocks
                successfull_attacks += 1      

        probability_of_success.append(successfull_attacks/ATTEMPTS)
    
    return hashrate_list, probability_of_success
