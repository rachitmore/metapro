import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def chart_data(symbol,start_date, end_date):
    data = yf.download(symbol + '.NS', start=start_date, end= end_date)
    fig = go.Figure()

    # Candlestick trace
    fig.add_trace(go.Candlestick(x=data.index,
                                        open=data['Open'],
                                        high=data['High'],
                                        low=data['Low'],
                                        close=data['Close'],
                                        name='Candlesticks',
                                        increasing_line_color='#00cc00',  # Green for increasing
                                        decreasing_line_color='#ff0000',  # Red for decreasing
                                        showlegend=False))

    # Add volume bars
    fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume', marker_color='#3333cc', opacity=0.9))

    # Add moving averages
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'].rolling(window=20).mean(),
                                    mode='lines', name='20-Day MA', line=dict(color='#ff9900')))  # Orange for 20-Day MA
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'].rolling(window=50).mean(),
                                    mode='lines', name='50-Day MA', line=dict(color='#ffcc00')))  # Yellow for 50-Day MA

    # Add Bollinger Bands
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'].rolling(window=20).mean() + 2 * data[
        'Close'].rolling(window=20).std(),
                                    mode='lines', name='Upper Bollinger Band', line=dict(color='#33cccc',
                                                                                        dash='dash')))  # Cyan for Upper BB
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'].rolling(window=20).mean() - 2 * data[
        'Close'].rolling(window=20).std(),
                                    mode='lines', name='Lower Bollinger Band', line=dict(color='#33cccc',
                                                                                        dash='dash')))  # Cyan for Lower BB

    # Customize layout with increased figure size and improved color scheme
    fig.update_layout(
        title=f'{symbol} Candlestick Chart with Volume and Indicators',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=True,
        template='plotly_dark',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='white')
        ),
        annotations=[
            # Add a text annotation to indicate the current stock price
            dict(x=data.index[-1], y=data['Close'].iloc[-1],
                    xref="x", yref="y",
                    text=f"Rs {data['Close'].iloc[-1]:.2f}",
                    showarrow=True,
                    arrowhead=2,
                    ax=0,
                    ay=-40,
                    font=dict(color='white')
                    )
        ],
        # Increase figure size
        height=600,
        width=1000
    )

    # Add custom buttons for user interactions
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(label="Reset Zoom",
                            method="relayout",
                            args=["xaxis.range[0]", None]),
                    dict(label="Zoom In",
                            method="relayout",
                            args=["xaxis.range[0]", "xaxis.range[1]"]),
                ],
                font=dict(color='white')
            ),
        ]
    )

    # Calculate and add MACD traces to the chart
    try:
        short_window = 12
        long_window = 26
        signal_window = 9
        short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
        long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
        macd = short_ema - long_ema
        signal = macd.ewm(span=signal_window, adjust=False).mean()

        # Add MACD trace to the chart
        fig.add_trace(go.Scatter(x=data.index, y=macd, mode='lines', name='MACD', line=dict(color='#ff00ff')))
        fig.add_trace(go.Scatter(x=data.index, y=signal, mode='lines', name='Signal', line=dict(color='#ff9900')))
    except Exception as e:
        print(f"An error occurred during MACD calculation: {str(e)}")

    plot_html = fig.to_html(full_html=False)

    return plot_html