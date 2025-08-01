# -*- coding: utf-8 -*-
"""endtoendchatbot

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AnYVlS2XJVvjdqFheSBoictYy7xMmtGV
"""

import os
import nltk
import ssl
import streamlit as st
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

ssl._create_default_https_context = ssl._create_unverified_context
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

intents = [
    {
        "tag": "greeting",
        "patterns": [
            "Hi", "Hello", "Hey", "Good morning", "Good evening", "What's up", 
            "How's it going?", "Yo", "Hi there", "Hey there", "Greetings", 
            "Hey buddy", "What's new?", "How are you?"
        ],
        "responses": [
            "Hello! 👋 I'm here to help you understand trading and investing. How can I assist you today?",
            "Hi there! Whether you're a beginner or experienced investor, feel free to ask me anything about the stock market.",
            "Welcome! Looking to explore stocks, strategies, or tools? I'm here to help!"
        ]
    },
    {
        "tag": "goodbye",
        "patterns": [
            "Bye", "Goodbye", "See you", "Talk to you later", "Catch you later", 
            "I'm done for now", "That's all", "Peace out", "Later", "See ya", 
            "Ciao", "Thanks, bye"
        ],
        "responses": [
            "Goodbye! Wishing you profitable trades and smart investments!",
            "Take care! Don’t forget to stay updated on market news.",
            "See you later! Feel free to come back for more trading tips or queries anytime."
        ]
    },
    {
        "tag": "thanks",
        "patterns": [
            "Thanks", "Thank you", "Thanks a lot", "Much appreciated", 
            "I appreciate it", "Thanks for the info", "Cool, thanks", 
            "Thanks for your help", "That’s helpful"
        ],
        "responses": [
            "You're welcome! I'm always here to help you navigate the financial world.",
            "No problem at all. Investing is a journey—glad to be a part of yours!",
            "Happy to help! Let me know if you have more questions about trading or the stock market."
        ]
    },
    {
        "tag": "stock_price",
        "patterns": [
            "What is the stock price of Apple", "Check Tesla stock", 
            "Price of Google shares", "How much is Amazon trading at", 
            "Current price of Microsoft", "Tell me the stock price of Infosys", 
            "What’s the share price of TCS", "How’s Reliance doing today", 
            "Price of HDFC shares", "Show me the stock price of Netflix", 
            "Get stock quote for Meta"
        ],
        "responses": [
            "I currently don't fetch real-time data. For live stock prices, please check financial apps like Google Finance, Yahoo Finance, TradingView, or your broker’s app like Zerodha, Groww, or Robinhood.",
            "Stock prices change every second during market hours. It's best to check reliable platforms for the latest updates."
        ]
    },
    {
        "tag": "market_hours",
        "patterns": [
            "What are stock market hours", "When does the market open", 
            "When does trading start", "Is the market open now", 
            "Trading hours in India", "When does NSE open", 
            "What time does NYSE open", "Stock market closing time", 
            "What’s the timing for BSE"
        ],
        "responses": [
            "In India, the stock market (NSE/BSE) is open from 9:15 AM to 3:30 PM IST, Monday to Friday.",
            "In the U.S., NYSE and NASDAQ are open from 9:30 AM to 4:00 PM EST, excluding public holidays.",
            "There’s also a pre-market (9:00 AM - 9:15 AM IST) and post-market (3:30 PM - 4:00 PM IST) session in India for order placement."
        ]
    },
    {
        "tag": "buy_stock",
        "patterns": [
            "How do I buy stocks", "Where can I buy shares", 
            "What app to use for trading", "Can I invest in stocks online", 
            "Best way to buy stocks", "What platforms can I use to trade", 
            "How to start buying stocks", "Is Zerodha good for beginners", 
            "Can I invest through Upstox"
        ],
        "responses": [
            "To buy stocks, you need a Demat and trading account with a registered broker like Zerodha, Upstox, Groww, or Angel One. After verification, you can add funds and place orders directly through their app or website.",
            "Most brokers provide easy-to-use platforms where you can search for a stock, place buy/sell orders, and track performance in real-time.",
            "As a beginner, consider starting with simple apps like Groww or Zerodha which offer great user experience and educational tools."
        ]
    },
    {
        "tag": "investing_vs_trading",
        "patterns": [
            "What’s the difference between investing and trading", "Should I invest or trade", 
            "Is trading better than investing", "Difference between trader and investor", 
            "What’s long-term investing", "What’s intraday trading"
        ],
        "responses": [
            "Investing means buying stocks with a long-term perspective, focusing on value and company fundamentals. It’s ideal for wealth creation over years.",
            "Trading is short-term—buying and selling stocks frequently to take advantage of price movements. It requires quick decisions and active monitoring.",
            "If you're looking for slow and steady growth, investing is better. If you prefer quick profits and understand risks, trading may be suitable."
        ]
    },
    {
        "tag": "stock_recommendation",
        "patterns": [
            "Which stock should I buy", "Best stocks to invest in", 
            "What are the top stocks today", "Any stock recommendations", 
            "Should I invest in TCS", "Is Reliance a good stock", 
            "What are blue chip stocks", "Tell me good stocks to buy now"
        ],
        "responses": [
            "I don’t provide specific stock picks, but generally, blue-chip companies like TCS, Infosys, HDFC, and Reliance are stable and have strong fundamentals.",
            "Consider diversifying into sectors like IT, pharma, banking, and energy. You can also look into ETFs or mutual funds for diversified exposure.",
            "Always research a company’s financials, future growth, industry position, and current valuation before buying."
        ]
    },
    {
        "tag": "risk_management",
        "patterns": [
            "How to manage risk in trading", "Tips for reducing losses", 
            "What is stop-loss", "How to avoid big losses in stock market", 
            "What are risk management strategies", "Should I use a stop-loss", 
            "How to protect my capital in trading"
        ],
        "responses": [
            "Risk management is crucial in trading. Set a stop-loss on every trade to limit losses if the price moves against you.",
            "Avoid putting all your capital into one trade. Diversify across different stocks or sectors.",
            "Never invest money you can’t afford to lose. Stick to a predefined plan and avoid emotional decisions during market volatility."
        ]
    },
    {
        "tag": "portfolio",
        "patterns": [
            "What is a stock portfolio", "How to build a portfolio", 
            "Diversify investments", "What should be in my portfolio", 
            "How many stocks should I own", "Is diversification important", 
            "Best way to build a beginner portfolio"
        ],
        "responses": [
            "A portfolio is your collection of investments—stocks, mutual funds, ETFs, and other financial instruments.",
            "For a balanced portfolio, consider a mix of large-cap (stable), mid-cap (moderate growth), and small-cap (high risk/high return) stocks.",
            "Diversification helps reduce risk—spread your investment across different sectors and asset classes."
        ]
    },
    {
        "tag": "dividends",
        "patterns": [
            "What are dividends", "Do stocks give income", 
            "How do dividends work", "Which companies pay dividends", 
            "What is dividend yield", "Can I earn monthly income from stocks"
        ],
        "responses": [
            "Dividends are profits that companies share with shareholders, usually on a quarterly basis. They are like interest paid on your stock investment.",
            "Not all companies pay dividends. Typically, well-established companies with stable earnings pay them regularly.",
            "Dividend yield is the annual dividend divided by the stock price. A higher yield may indicate good passive income potential."
        ]
    },
    {
        "tag": "credit_score",
        "patterns": [
            "What is a credit score", "How do I check my credit score", 
            "How can I improve my credit score", "Is credit score important for investing", 
            "Credit score for opening trading account"
        ],
        "responses": [
            "A credit score is a number between 300-900 that reflects your creditworthiness. It’s used by banks and lenders to decide if you’re eligible for loans or credit cards.",
            "You can check your credit score through websites like CIBIL, Experian, or CRIF High Mark. In the U.S., use Credit Karma or Equifax.",
            "Although a good credit score helps with loan approvals, it's not required for investing or trading."
        ]
    }
]

# Create the vectorizer and classifier
vectorizer = TfidfVectorizer()
clf = LogisticRegression(random_state=0, max_iter=10000)

# Preprocess the data
tags = []
patterns = []
for intent in intents:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)

# training the model
x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

def chatbot(input_text):
    input_text = vectorizer.transform([input_text])
    tag = clf.predict(input_text)[0]
    for intent in intents:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            return response

counter = 0

def main():
    global counter
    st.title("Chatbot")
    st.write("Welcome to the chatbot. Please type a message and press Enter to start the conversation.")

    counter += 1
    user_input = st.text_input("You:", key=f"user_input_{counter}")

    if user_input:
        response = chatbot(user_input)
        st.text_area("Chatbot:", value=response, height=100, max_chars=None, key=f"chatbot_response_{counter}")

        if response.lower() in ['goodbye', 'bye']:
            st.write("Thank you for chatting with me. Have a great day!")
            st.stop()

if __name__ == '__main__':
    main()
