from csv import DictWriter
import pandas as pd
import yfinance as yf
import logging


def fetch_stock_information():
    logging.basicConfig(format='%(asctime)s %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    logger.info(">> Reading stock data..")
    stocks = pd.read_csv("data/nse_bse_merged.csv")
    stocks.sort_values(by='SYMBOL', ascending=True, inplace=True)
    logger.info(">> Stock data read.")

    headers = ['symbol', 'listed_on', 'long_name', 'short_name', 'sector', 'sector_key', 'sector_disp', 'industry', 'industry_key',
               'industry_disp']
    logger.info(">> Writing headers..")
    
    with open('data/listed_stocks.csv', 'w', newline='', encoding='UTF-8') as file:
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        file.close()
    logger.info(">> Headers written.")

    def write_data(stock_data):
        logger.info(f">> Writing row for {stock_data.get("symbol")} ...")
        with open('data/listed_stocks.csv', 'a', newline="", encoding="UTF-8") as data_file:
            row_writer = DictWriter(data_file, fieldnames=headers)
            row_writer.writerow(stock_data)
            file.close()
        logger.info(f">> Row for {stock_data.get("symbol")} written.")

    for stock in stocks.itertuples(index=False):

        current_stock_data = dict()
        symbol = str(stock.SYMBOL)
        source = str(stock.SOURCE)

        ext = 'NS' if source == 'NSE' else "BO"
        logger.info(f">> Fetching data for {symbol}")
        data = yf.Ticker(f'{symbol}.{ext}')
        logger.info(f">> Fetched data for {symbol}")

        current_stock_data['symbol']        = symbol
        current_stock_data['listed_on']     = source
        current_stock_data['sector']        = data.info.get('sector')
        current_stock_data['sector_key']    = data.info.get('sectorKey')
        current_stock_data['sector_disp']   = data.info.get('sectorDisp')
        current_stock_data['industry']      = data.info.get('industry')
        current_stock_data['industry_key']  = data.info.get('industryKey')
        current_stock_data['industry_disp'] = data.info.get('industryDisp')
        current_stock_data['long_name']     = data.info.get('longName')
        current_stock_data['short_name']    = data.info.get('shortName')

        write_data(current_stock_data)

if __name__ == "__main__":
    fetch_stock_information()



# ['address1', 'address2', 'city', 'zip', 'country', 'phone', 'fax', 'website', 'industry', 'industryKey', 'industryDisp', 'sector', 'sectorKey', 'sectorDisp', 'longBusinessSummary', 'fullTimeEmployees', 'companyOfficers', 'compensationAsOfEpochDate', 'executiveTeam', 'maxAge', 'priceHint', 'previousClose', 'open', 'dayLow', 'dayHigh', 'regularMarketPreviousClose', 'regularMarketOpen', 'regularMarketDayLow', 'regularMarketDayHigh', 'dividendRate', 'dividendYield', 'exDividendDate', 'payoutRatio', 'beta', 'trailingPE', 'volume', 'regularMarketVolume', 'averageVolume', 'averageVolume10days', 'averageDailyVolume10Day', 'bid', 'ask', 'bidSize', 'askSize', 'marketCap', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'allTimeHigh', 'allTimeLow', 'priceToSalesTrailing12Months', 'fiftyDayAverage', 'twoHundredDayAverage', 'trailingAnnualDividendRate', 'trailingAnnualDividendYield', 'currency', 'tradeable', 'enterpriseValue', 'profitMargins', 'floatShares', 'sharesOutstanding', 'heldPercentInsiders', 'heldPercentInstitutions', 'impliedSharesOutstanding', 'bookValue', 'priceToBook', 'lastFiscalYearEnd', 'nextFiscalYearEnd', 'mostRecentQuarter', 'earningsQuarterlyGrowth', 'netIncomeToCommon', 'trailingEps', 'lastSplitFactor', 'lastSplitDate', 'enterpriseToRevenue', 'enterpriseToEbitda', '52WeekChange', 'SandP52WeekChange', 'lastDividendValue', 'lastDividendDate', 'quoteType', 'currentPrice', 'recommendationKey', 'totalCash', 'totalCashPerShare', 'ebitda', 'totalDebt', 'quickRatio', 'currentRatio', 'totalRevenue', 'debtToEquity', 'revenuePerShare', 'returnOnAssets', 'returnOnEquity', 'grossProfits', 'freeCashflow', 'operatingCashflow', 'earningsGrowth', 'revenueGrowth', 'grossMargins', 'ebitdaMargins', 'operatingMargins', 'financialCurrency', 'symbol', 'language', 'region', 'typeDisp', 'quoteSourceName', 'triggerable', 'customPriceAlertConfidence', 'hasPrePostMarketData', 'firstTradeDateMilliseconds', 'regularMarketChange', 'regularMarketDayRange', 'fullExchangeName', 'averageDailyVolume3Month', 'fiftyTwoWeekLowChange', 'fiftyTwoWeekLowChangePercent', 'fiftyTwoWeekRange', 'fiftyTwoWeekHighChange', 'fiftyTwoWeekHighChangePercent', 'fiftyTwoWeekChangePercent', 'earningsTimestampStart', 'earningsTimestampEnd', 'earningsCallTimestampStart', 'earningsCallTimestampEnd', 'isEarningsDateEstimate', 'epsTrailingTwelveMonths', 'fiftyDayAverageChange', 'fiftyDayAverageChangePercent', 'twoHundredDayAverageChange', 'corporateActions', 'regularMarketTime', 'exchange', 'messageBoardId', 'exchangeTimezoneName', 'exchangeTimezoneShortName', 'gmtOffSetMilliseconds', 'market', 'esgPopulated', 'marketState', 'twoHundredDayAverageChangePercent', 'sourceInterval', 'exchangeDataDelayedBy', 'cryptoTradeable', 'regularMarketChangePercent', 'regularMarketPrice', 'shortName', 'longName', 'trailingPegRatio']