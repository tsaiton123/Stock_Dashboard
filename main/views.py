# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Stock
from .forms import StockForm
import requests
import pandas as pd
import yfinance as yf
from transformers import pipeline

def get_news(stock_ticker, num_articles=10, api_key='YOUR_NEWSAPI_KEY'):
    url = f'https://newsapi.org/v2/everything?q={stock_ticker}&apiKey={api_key}&pageSize={num_articles}'
    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])
    return articles

def dashboard(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock_ticker = form.cleaned_data['ticker']
            # Check if the stock symbol already exists
            if not Stock.objects.filter(ticker=stock_ticker).exists():
                form.save()
            else:
                messages.info(request, f"Stock {stock_ticker} already exists.")
            # form.save()
            # return redirect('dashboard')
    else:
        form = StockForm()
    
    stocks = Stock.objects.all()
    stock_data = []
    
    for stock in stocks:
        # Fetch stock price data (you need to replace with an actual API)
        stock_ticker = stock.ticker
        # stock_price_url = f'https://api.example.com/stock/{stock_ticker}/price'
        # stock_price_response = requests.get(stock_price_url).json()
        stock_price_response = yf.download(stock_ticker, period='1d', interval='1h').tail(10)
        
        # Fetch news data
        news_articles = get_news(stock_ticker, api_key='66824c56e5f54659ab9a92b6995c471f')
        
        # Sentiment analysis
        classifier = pipeline("sentiment-analysis")
        sentiment_score = 0
        for article in news_articles:
            result = classifier(article['title'])
            if result[0]['label'] == 'POSITIVE':
                sentiment_score += result[0]['score']
            else:
                sentiment_score -= result[0]['score']
        
        stock_data.append({
            'id': stock.id,  # Add 'id' to stock data
            'ticker': stock_ticker,
            'price': stock_price_response['Open'],
            'news': news_articles,
            'sentiment_score': sentiment_score
        })
    
    context = {
        'form': form,
        'stock_data': stock_data
    }
    
    return render(request, 'dashboard.html', context)

def delete_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)  # New view to handle stock deletion
    stock.delete()
    messages.success(request, f"Stock {stock.ticker} has been deleted.")
    return redirect('dashboard')