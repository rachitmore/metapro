# trading/views.py
from django.shortcuts import render
from .forms import BacktestForm
from .strategies import apply_strategy
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def backtest(request):
    if request.method == 'POST':
        form = BacktestForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            strategy_name = form.cleaned_data['strategy_name']

            # Fetch historical price data (replace with actual data source)
            price_data = PriceData.objects.filter(symbol=symbol, date__range=(start_date, end_date))
            df = pd.DataFrame(list(price_data.values()))

            # Apply selected strategy
            df = apply_strategy(df, strategy_name)

            # Plot and save the figure
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df['Close'], label='Close Price')
            ax.plot(df[df['Signal'] == 1].index, df['Close'][df['Signal'] == 1], '^', markersize=10, color='g', label='Buy Signal')
            ax.plot(df[df['Signal'] == -1].index, df['Close'][df['Signal'] == -1], 'v', markersize=10, color='r', label='Sell Signal')
            ax.set_title(f'Backtest Results - {strategy_name}')
            ax.set_xlabel('Date')
            ax.set_ylabel('Close Price')
            ax.legend()
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()

            # Convert the plot to base64 for display in HTML
            plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

            return render(request, 'trading_strategies/backtest_results.html', {'plot_data': plot_data})

    else:
        form = BacktestForm()

    return render(request, 'trading_strategies/backtest.html', {'form': form})
