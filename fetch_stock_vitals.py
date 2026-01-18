import json
from requests import get
import logging
from Config import Config
import yfinance as yf
from utils.get_financial_dataframes import get_financial_dataframes
from utils.FinancialMetricsCalculator import FinancialMetricsCalculator

def fetch_stock_vitals(ticker: str, source: str) -> None:
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(message)s')

    logger.info(f">> Fetching vitals for {ticker}")
    querystring   = {"name": ticker}
    headers       = {"X-Api-Key": Config.X_API_KEY}
    url           = f"{Config.X_API_URL}{Config.X_API_STOCK_ENDPOINT}"
    response      = get(url, headers=headers, params=querystring)
    stock_data    = response.json()
    current_price = stock_data.get('currentPrice').get(source.upper(), "Not found")
    one_year_high = stock_data.get('yearHigh')
    one_year_low  = stock_data.get('yearLow')

    print(current_price)
    print(one_year_low)
    print(one_year_high)
    # Decompose the financial metrics into annual (for YoY) and interim (for QoQ) metrics
    df_annual, df_interim = get_financial_dataframes(stock_data.get('financials'))


    annual_financials = FinancialMetricsCalculator(df_annual)
    annual_metrics    = annual_financials.get_all_metrics(period_days=365, growth_lag=1)

    # 2. Initialize for Interim Data (91.25 days, lag=4 for YoY quarter growth)
    interim_financials = FinancialMetricsCalculator(df_interim)
    interim_metrics    = interim_financials.get_all_metrics(period_days=91.25, growth_lag=4)

    # 3. View Results
    interim_metrics.to_csv(f"data/{ticker}-interim_metrics.csv")
    annual_metrics.to_csv(f"data/{ticker}-annual_metrics.csv")

    # stock_vitals = yf.Ticker(f"{ticker}.NS").info
    # current_price = stock_vitals.get("currentPrice")
    # one_year_high = stock_vitals.get("fiftyTwoWeekHigh")
    # one_year_low  = stock_vitals.get("fiftyTwoWeekLow")
    #
    # print(current_price)
    # print(one_year_high)
    # print(one_year_low)



if __name__ == "__main__":
    fetch_stock_vitals("TATASTEEL", "NSE")
    fetch_stock_vitals("NHPC", "NSE")

