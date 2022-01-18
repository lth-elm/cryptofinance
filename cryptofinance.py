import json
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

st.sidebar.title('Simulation')
simulation = st.sidebar.selectbox('Choose the simulation you want to run.', ('Home', 'Proof of Work', 'Attack 1 : One plus two', 'Attack 2 : Selfish mining', 'Attack 3 : Double spending'))
st.header(simulation)


if simulation == "Home":
    st.subheader('Subheader ?')
    st.write('Describe the project...')


if simulation == "Proof of Work":
    st.subheader('Subheader ?')
    st.write('Add description...')
    st.image('pow/pow_output.png')


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



# """
# ___
# markdown :
# # Header
# ## Subheader
# ___
# """

# list = [1, 2, 3]
# st.write(list)

# st.image('./output.png')
