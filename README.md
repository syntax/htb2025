# quinten - your personal crypto portfolio manager

Made in 24 hours during Hack the Burgh 2025.
(this readme was written after 40mins sleep, so apologies.)

This project aims to act as a personal crypto portfolio manager, powered by AI. In particular, cryptocurrency is an assert class that is scary for many, and this tooling aims to make this investment oppurtunity more accessible. Calling and VoP interactions with our AI agent make this more accessible to the older crowd. Deeply investigated sustainbility criterion for investment portfolios make cryptocurrency more appealing to the enviromentally-concious younger crowds, who have previously been put off by gross power consumption involves in PoW coins.

## dependencies and tooling used

We use a stack of Python and Flask for the backend, and Vite, Typescript and react for the frontend. The majority of our external dependencies are on external APIs, including CoinGecko, Yahoo Finance, Twilio and OpenAI. The frontend uses npm for package management, and MUI is used to abstract some CSS and styling. In Python, we use Flask for hosting our webapp. The database is run using SQLAlchemy. Pandas, Numpy and SKlearn libraries are used for statistical methods to suggest an potential portolio based on the users risk appetite and other factors. nltk and Vader are used for sentiment analysis. For constructing predictions on stock prices, we use an LSTM made possible through tensorflow and sklearn.

We have used copilot to assist in development with this project.

### limitations/abstractions to note

Quite a lot of the data required for this project relies on API's which are often rate limited or behind conisderable paywalls. Where we have found this significantly stunt development, data has been mocked out and LLM's, such as ChatGPT 4o have been used, for example, in tweet data generation.

## to run;

### backend;

requirements are specified in the text file.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py                  // should open up on localhost:5000
```
### frontend

```bash
npm install
npm run dev
```