import csv
import json
from this import d
import requests
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from selfish_mining import selfish_mining
from double_spending import double_spending
from att_one_plus_two import att_one_plus_two


# =========== FUNCTION ZONE ===========

def attack_length(time):
    days = time // (24 * 3600)
    time = time % (24 * 3600)
    hours = time // 3600
    time %= 3600
    minutes = time // 60
    return days, hours, minutes


# =========== INTERFACE ZONE ===========

st.title('Cryptofinance')

st.sidebar.image("logo/Logo_ESILV_170x170.png", width=100)
st.sidebar.title('Simulation')
simulation = st.sidebar.selectbox('Choose the simulation you want to run.', ('Home', 'Proof of Work', 'Attack 1 : One plus two', 'Attack 2 : Selfish mining', 'Attack 3 : Double spending'))
st.header(simulation)



if simulation == "Home":
    st.subheader('Description')
    """
    This project aims to simulate concepts related to **bitcoin mining** and its notion of **proof of work**
    but also **attack strategies** in which our interest is to visualize the critical levels of **profitability** 
    and the **hash power** needed to achieve it.

    The results are from research papers by teacher and researcher Cyril Grunspan (Da Vinci Research Center) 
    and Ricardo Perez-Marco : *<links>*

    The understanding of this paper and its visual presentation in this website was conducted by *<Laith El Mershati>*, 
    student of the **Enginnering School De Vinci Paris** (ESILV), and is part of a school project.
    """




if simulation == "Proof of Work":
    st.subheader('Mining time')

    """
    We are going to conduct a proof of work **mining** where we want to see how the **average time** needed to 
    find the solution evolves with the **difficulty adjustment**. 
    
    For that we will be running *<that code>* which from this challenge ```5JskLFx82fGh7eFP3c12XXX``` will add a 
    generated random nonce and then hash the whole new variable until we the target of *x* 0's at the beginning 
    of the new hash is obtained.
    """

    with open('pow/pow_time_values.csv', newline='') as f:
        reader = csv.reader(f)
        data_time = list(reader)[0]
    
    data_time.remove('')
    for i in range(len(data_time)):
        data_time[i] = float(data_time[i])

    targets = list(range(1, len(data_time) + 1, 1))

    fig, ax = plt.subplots(figsize=(5, 3))
    plt.title('Time required to find the hash solution according to target', fontsize=9)
    ax.plot(targets, data_time, '-ok')
    ax.set_xlabel('0 target', fontsize=8)
    ax.set_ylabel('Time (s)', fontsize=8)
    ax.legend()
    st.pyplot(fig=plt)

    st.write("Here is a better reading of the above values.")
    st.write(data_time)

    """
    One can easily notice an exponential trend between the number of 0's required before the hash 
    and the time needed to achieve it, which tends to increase exponentially.
    """

    st.subheader('Exponential law')

    """
    Let's repeat the same task 10 000 times but this time with a target of 3 only, 
    here is a distribution of the time it took for each execution. (Code at this *<link>*)
    """

    with open('pow/expow_distribution_values.csv', newline='') as f:
        reader = csv.reader(f)
        time_result = list(reader)[0]
    
    for i in range(len(time_result)):
        time_result[i] = float(time_result[i])

    x = [i for i in range(1, len(time_result)+1, 1)]
    fig, ax = plt.subplots(figsize=(5, 3))
    plt.title('Distribution of the time took to find the hash solution for all the executions', fontsize=9)
    ax.plot(x, time_result, '-ok', color='darkblue', markersize=2)
    ax.set_xlabel('Executions', fontsize=8)
    ax.set_ylabel('Time (s)', fontsize=8)
    ax.legend()
    st.pyplot(fig=plt)

    """
    Obviously at a certain point it becomes more unusual that the search time exceeds a certain threshold.

    From this we can then deduce the probability of meeting the target after a certain time. 
    The computations are available in the code, the given results reflect in an obvious way an exponential law, 
    according to the research paper the *lambda* parameter has a value of 1/600.
    """

    base = time_result[0]
    end = time_result[-1]
    interval = end - base
    steps = interval/(len(time_result)/2)

    rangeprob = [i for i in np.arange(base, end, steps)]
    rangeprob.pop()
    probr = []

    for i in rangeprob:
        result = [x for x in time_result if x >= i]
        probr.append(len(result)/10000)

    fig, ax = plt.subplots(figsize=(5, 3))
    plt.title('Probability to find the target after x seconds', fontsize=9)
    ax.plot(rangeprob, probr, '-ok', color='darkred', markersize=2)
    ax.set_xlabel('Time (s)', fontsize=8)
    ax.set_ylabel('Probability', fontsize=8)
    ax.legend()
    st.pyplot(fig=plt)

    st.write("We can try and confirm the *lambda* parameter value with a study.")



if simulation == "Attack 1 : One plus two":

    # ====== SIDEBAR ZONE

    cycle = st.sidebar.slider('Cycle', min_value=100, max_value=10000, value=2000, step=100)
    show_thq = st.sidebar.checkbox('Show theoretical output', value=False)
    hash_power_list = np.arange(0.30,0.49,0.01)

    result_list, theoretical_list = att_one_plus_two(cycle, hash_power_list)

    # ====== MAIN ZONE

    st.subheader('Subheader ?')
    st.write('Add description...')
    plt.title('One plus two attack profitability')

    fig, ax = plt.subplots()
    ax.plot(hash_power_list, hash_power_list, color='blue', label='Honest mining')
    ax.plot(hash_power_list, result_list, color='crimson', label='Attacker mining')
    if show_thq:
        ax.plot(hash_power_list, theoretical_list, color='green', label='Theoretical attacker mining')
    ax.set_xlabel("Hashrate share (%)")
    ax.set_ylabel("Profitability over network (%)")
    ax.legend()

    st.pyplot(fig=plt)



if simulation == "Attack 2 : Selfish mining":

    # ====== SIDEBAR ZONE

    cycle = st.sidebar.slider('Cycle', min_value=100, max_value=10000, value=5000, step=100)
    days, hours, minutes = attack_length(cycle*10*60)
    attack_duration = str(days) + ' days ' if days > 1 else (str(days) + ' day ' if days == 1 else '')
    attack_duration += str(hours) + ' hours ' if hours > 1 else (str(hours) + ' hour ' if hours == 1 else '')
    attack_duration += str(minutes) + ' minutes' if minutes > 1 else (str(minutes) + ' minute' if minutes == 1 else '')
    st.sidebar.write('**Attack length** : ', attack_duration)

    connectivity = st.sidebar.slider('Connectivity (%)', min_value=0, max_value=100, value=50, step=2)
    connectivity = round(connectivity/100, 2)

    r = requests.get('https://api.coinbase.com/v2/prices/spot?currency=USD')
    data = json.loads(r.text)
    current_btc_price = int(float(data['data']['amount']))
    btc_price = st.sidebar.number_input('BTC price', min_value=100, max_value=9000000, value=current_btc_price, step=1)

    btc_blockreward = st.sidebar.number_input('BTC block reward', min_value=0.0, max_value=50.0, value=6.25)

    hashrates, profitability_ratios, selfish_profits = selfish_mining(cycle, connectivity, btc_price, btc_blockreward)
    selfish_profits = list(map(lambda x: x/1e6, selfish_profits)) # convert to million

    # ====== MAIN ZONE

    st.subheader('Subheader ?')
    st.write('Add description...')

    fig, ax = plt.subplots()
    plt.title('Selfish mining expected profit')

    h = [i for i in np.arange(0, 0.6, 0.1)]
    ax.plot(h, h, label='Honest mining')
    ax.plot(hashrates, profitability_ratios, label='Selfish mining', color='crimson')
    ax.set_xlabel('Hashrate share (%)')
    ax.set_ylabel('Profitability over network (%)')
    ax.legend()

    ax2 = ax.twinx()
    ax2.plot(hashrates, selfish_profits, ':', color='crimson')
    ax2.set_ylabel('Profit expectancy (Million $)')

    st.pyplot(fig=plt)



if simulation == "Attack 3 : Double spending":

    # ====== SIDEBAR ZONE

    attempts = st.sidebar.slider('Number of attempts', min_value=100, max_value=10000, value=5000, step=100)
    z = st.sidebar.slider('Z confirmation blocks', min_value=2, max_value=20, value=6, step=1)
    limit = st.sidebar.slider('Difference of blocks for giving up attack', min_value=1, max_value=50, value=6, step=1)

    hashrates, probability_of_success = double_spending(attempts, z, limit)
    probability_of_success = list(map(lambda x: x*100, probability_of_success)) # %

    # ====== MAIN ZONE

    st.subheader('Subheader ?')
    st.write('Add description...')

    fig, ax = plt.subplots()
    plt.title('Double spending chance of success')

    ax.plot(hashrates, probability_of_success, color='crimson')
    ax.set_xlabel('Hashrate share (%)')
    ax.set_ylabel('Probability of success (%)')
    ax.legend()

    st.pyplot(fig=plt)
