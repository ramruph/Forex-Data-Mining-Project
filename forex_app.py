import streamlit as st
import pandas as pd
import utils
import plotly.express as px
import pickle
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt



# Function to plot candlestick charts
def plot_candles(fig, df_plot, pair_name, granularity, row, col):
    # Add Candlestick trace
    fig.add_trace(
        go.Candlestick(
            x=df_plot['time'], 
            open=df_plot['mid_o'], 
            high=df_plot['mid_h'], 
            low=df_plot['mid_l'], 
            close=df_plot['mid_c'],
            line=dict(width=1), opacity=1,
            increasing_fillcolor='#24A06B',
            decreasing_fillcolor='#CC2E3C',
            increasing_line_color='#2EC886',
            decreasing_line_color='#FF3A4C'
        ),
        row=row, col=col
    )
    # Update axes and layout for this subplot
    fig.update_xaxes(
        title_text=f'{pair_name} {granularity}',
        gridcolor='#1f292f',
        showgrid=True,
        fixedrange=True,
        rangeslider=dict(visible=False),
        rangebreaks=[{'bounds': ['sat', 'mon']}],  # remove weekend gaps
        row=row, col=col
    )
    fig.update_yaxes(gridcolor='#1f292f', showgrid=True, row=row, col=col)

# Set the page config to wide mode with a dark theme
st.set_page_config(layout="wide", page_title="Forex Trading Candlestick Dashboard")

# Streamlit UI
st.title('Forex Trading Dashboard')

# Currency pair selection
pair_list = ['AUD_USD', 'EUR_USD', 'GBP_USD', 'NZD_USD', 'USD_CAD', 'USD_CHF', 'USD_JPY']
selected_pair = st.selectbox('Select a Currency Pair', pair_list)
granularities = ["M5", "H1", 'H4']

# Create a subplot figure with 1 row and 3 columns
fig = make_subplots(rows=1, cols=3, subplot_titles=[f'{selected_pair} {gran}' for gran in granularities])

# Read and plot data for each granularity
for i, granularity in enumerate(granularities, start=1):
    try:
        # Load data here, replace this with actual data loading
        df = pd.read_pickle(utils.get_hist_data_filename(selected_pair, granularity)) # Adjust according to your data source
        # df['time'] = pd.to_datetime(df['time'])  # Ensure 'time' column is datetime
        df_plot = df.iloc[-250:]  # Select the most recent 250 data points to plot
        plot_candles(fig, df_plot, selected_pair, granularity, 1, i)
    except FileNotFoundError:
        st.error(f"Data file for {selected_pair} {granularity} not found.")

# Update overall figure layout
fig.update_layout(
    width=700,  # Adjust width to fit your Streamlit layout
    height=500,  # Adjust height based on your preference
    margin=dict(l=10, r=10, b=10, t=30),
    font=dict(size=10, color='#e1e1e1'),
    paper_bgcolor='#1e1e1e',
    plot_bgcolor='#1e1e1e',
    showlegend=False,
    title_text=f'Candlestick Charts for {selected_pair}'
)

st.plotly_chart(fig, use_container_width=True)


st.header('Model Evaluation')
# selected_pair = st.selectbox('Select a Currency Pair', ['AUD_USD', 'EUR_USD', 'GBP_USD', 'NZD_USD', 'USD_CAD', 'USD_CHF', 'USD_JPY'])

try:
    # Load model data
    with open(f'model_results/{selected_pair}_mod_pred.pkl', 'rb') as f:
        data = pickle.load(f)

    model = data['model']
    accuracy = data['accuracy']
    report = data['report']

    st.write(f"### Accuracy for {selected_pair}: {accuracy:.2%}")

    st.write("### Classification Report")
    st.json(report)

    # Feature importance
    st.write("### Feature Importance")
    fig, ax = plt.subplots()
    ax.bar(range(len(model.coef_[0])), model.coef_[0])
    ax.set_xticks(range(len(model.coef_[0])))
    ax.set_xticklabels(['volume', 'returns', 'volatility', 'ma50', 'rsi'], rotation=45)
    ax.set_title('Feature Coefficients')
    st.pyplot(fig)
except Exception as e:
    st.error(f"Failed to load model data: {str(e)}")