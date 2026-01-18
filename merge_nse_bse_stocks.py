

def merge_nse_bse_stocks():
    import pandas as pd
    import logging
    logging.basicConfig(format='%(asctime)s %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    nse_data = pd.read_csv('data/NSE_MASTER.csv')
    logger.info(">> Read NSE stocks.")
    bse_data = pd.read_csv('data/BSE_MASTER.CSV')
    logger.info(">> Read BSE stocks")

    logger.info(">> Filtering eligible stocks...")
    nse_stocks = nse_data[(nse_data['SERIES'] == 'EQ') | (nse_data['SERIES'] == 'BE')]
    bse_stocks = bse_data[((bse_data['SERIES'] == 'A') | (bse_data['SERIES'] == 'B'))]
    logger.info(">> Stocks filtered.")

    logger.info(">> Merging stocks..")
    df_combined = pd.concat([nse_stocks, bse_stocks], ignore_index=True)

    df_combined['SOURCE'] = pd.Categorical(df_combined['SOURCE'], categories=['NSE', 'BSE'], ordered=True)
    df_combined = df_combined.sort_values('SOURCE')
    logger.info(">> Dropping duplicates...")
    df_merged = df_combined.drop_duplicates(subset=['ISIN_NUMBER'], keep='first')
    logger.info(">> Duplicates dropped.")
    df_merged = df_merged.reset_index(drop=True)
    logger.info(">> Stocks merged.")
    logger.info(">> Writing to file..")
    df_merged.to_csv("nse_bse_merged.csv")
    logger.info(">> File Written. Shutting down.")

if __name__ == "__main__":
    merge_nse_bse_stocks()
