import random
import numpy as np


def selfish_mining(cycle, connectivity, btc_val, btc_blockreward):
    hashrate_list = []
    profitability_ratio_list = []
    selfish_profit_list = []

    for hashrate in np.arange(0, 0.49, 0.01):
        hashrate_list.append(hashrate)

        # SET CONSTANTS AND VARIABLES

        CYCLE = cycle # attack cycles
        CONNECTIVITY = connectivity

        BTC_VAL = btc_val
        BTC_BLOCK_REWARD = btc_blockreward

        S = 0 # selfish blocks
        H = 0 # honest blocks

        mainchain = 0 # blocks on the main chain before the cycle attack starts
        selfish_profit = 0 # selfish miner profits 

        while(mainchain < CYCLE):  
            edge = S - H # selfish blocks in advance
            
            p = random.uniform(0, 1)
            if(p < hashrate): # Selfish miner finds the first block
                S += 1

                # Start a selfish mining attack
                while(mainchain <= CYCLE):
                    p = random.uniform(0, 1)

                    if(p < hashrate): # pile up selfish blocks until we get catched up
                        S += 1
                    else:
                        H +=1                    
                        edge = S - H # new selfish miner edge

                        if(edge == 0): # We got catched up
                            mainchain += 1
                            p = random.uniform(0,1)

                            if(p <= CONNECTIVITY): # Our blocks get chosen by the other majority of miners
                                mainchain += S
                                selfish_profit += BTC_VAL * BTC_BLOCK_REWARD * S
                                H, S = 0, 0 # reset since all our blocks are pushed

                            else: # Our blocks don't get chosen by the other majority of miners
                                mainchain += H
                                H, S = 0, 0 # reset since all blocks are rejected

                        elif(edge == 1): # Only one advance
                            mainchain += S
                            selfish_profit += BTC_VAL * BTC_BLOCK_REWARD * S
                            H, S = 0, 0

                        elif(edge == -1): # Honest miner got the lead
                            mainchain += H
                            H, S = 0, 0

            else: # Honest miner finds the first block
                mainchain += 1
            
        profitability_ratio_list.append(selfish_profit/(mainchain * BTC_BLOCK_REWARD * BTC_VAL))
        selfish_profit_list.append(selfish_profit)

    return hashrate_list, profitability_ratio_list, selfish_profit_list
