import pandas as pd
import numpy as np


class FinancialMetricsCalculator:
    def __init__(self, df):
        """
        Initializes the calculator with a Pandas DataFrame.
        Expected Columns (from your JSON schema):
        - 'NetIncome', 'TotalRevenue', 'TotalAssets', 'TotalEquity'
        - 'TotalDebt', 'TotalCurrentLiabilities', 'TotalInventory'
        - 'CostofRevenueTotal', 'AccountsReceivable-TradeNet', 'AccountsPayable'
        - 'ProvisionforIncomeTaxes', 'InterestInc(Exp)Net-Non-OpTotal'
        - 'DilutedEPSExcludingExtraOrdItems'
        """
        self.df = df

    def _get_col(self, col_name):
        """Helper to safely get a column or return NaN series if missing."""
        if col_name in self.df.columns:
            return self.df[col_name]
        return pd.Series(np.nan, index=self.df.index)

    # --- Core Profitability Metrics ---

    def calculate_ebit(self):
        """
        EBIT = Net Profit + Taxes + Interest Expense
        Note: In the dataset, Interest is a negative value (Expense).
        We subtract it to add the absolute value back.
        """
        net_income = self._get_col('NetIncome')
        taxes      = self._get_col('ProvisionforIncomeTaxes')
        interest   = self._get_col('InterestInc(Exp)Net-Non-OpTotal')
        return net_income + taxes - interest

    def calculate_capital_employed(self):
        """Capital Employed = Total Assets - Current Liabilities"""
        return self._get_col('TotalAssets') - self._get_col('TotalCurrentLiabilities')

    def calculate_shareholder_equity(self):
        """Shareholder Equity (Total Equity)"""
        return self._get_col('TotalEquity')

    def calculate_eps(self):
        """Earnings Per Share (Directly from Data)"""
        return self._get_col('DilutedEPSExcludingExtraOrdItems')

    # --- Efficiency & Return Metrics ---

    def calculate_roce(self):
        """ROCE = EBIT / Capital Employed"""
        ebit = self.calculate_ebit()
        ce = self.calculate_capital_employed()
        return (ebit / ce) * 100

    def calculate_roe(self):
        """ROE = Net Profit / Shareholder Equity"""
        return (self._get_col('NetIncome') / self.calculate_shareholder_equity()) * 100

    def calculate_roa(self):
        """ROA = Net Profit / Total Assets"""
        return (self._get_col('NetIncome') / self._get_col('TotalAssets')) * 100

    def calculate_opm(self):
        """OPM = EBIT / Total Revenue"""
        return (self.calculate_ebit() / self._get_col('TotalRevenue')) * 100

    # --- Leverage & Solvency Metrics ---

    def calculate_de_ratio(self):
        """D/E Ratio = Total Debt / Shareholder Equity"""
        return self._get_col('TotalDebt') / self.calculate_shareholder_equity()

    # --- Operational Efficiency (CCC) ---

    def calculate_ccc(self, period_days=365):
        """
        Cash Conversion Cycle = DIO + DSO - DPO
        DIO = (Inventory / COGS) * Days
        DSO = (Receivables / Revenue) * Days
        DPO = (Payables / COGS) * Days
        """
        inventory = self._get_col('TotalInventory')
        cogs = self._get_col('CostofRevenueTotal')
        receivables = self._get_col('AccountsReceivable-TradeNet')
        revenue = self._get_col('TotalRevenue')
        payables = self._get_col('AccountsPayable')

        # Avoid division by zero
        if cogs.sum() == 0 or revenue.sum() == 0:
            return pd.Series(np.nan, index=self.df.index)

        dio = (inventory / cogs) * period_days
        dso = (receivables / revenue) * period_days
        dpo = (payables / cogs) * period_days

        return dio + dso - dpo

    # --- Growth Metrics ---

    def calculate_eps_growth(self, periods=1):
        """
        EPS Growth (YoY or QoQ)
        'periods' defines the lag:
        - Use 1 for Sequential Growth (Current vs Previous)
        - Use 4 for YoY Interim Growth (Current vs Same Qtr Last Year)
        """
        eps = self.calculate_eps()
        eps_prev = eps.shift(periods)
        # Formula: (Current - Prev) / abs(Prev)
        return ((eps - eps_prev) / eps_prev.abs()) * 100

    # --- Placeholders for Missing Market/Banking Data ---
    # These return NaN because the specific fields (Share Price, Volume)
    # are not present in the provided financials.json schema.

    def calculate_pe_ratio(self):
        """P/E = Share Price / EPS"""
        return pd.Series(np.nan, index=self.df.index)

    def calculate_peg_ratio(self):
        """PEG = P/E / EPS Growth"""
        return pd.Series(np.nan, index=self.df.index)

    def calculate_relative_volume(self):
        """Relative Volume = Today Vol / Avg Vol"""
        return pd.Series(np.nan, index=self.df.index)

    def calculate_nim(self):
        """Net Interest Margin (Banking Specific)"""
        return pd.Series(np.nan, index=self.df.index)

    def calculate_npa(self):
        """Non-Performing Assets (Banking Specific)"""
        return pd.Series(np.nan, index=self.df.index)

    def calculate_casa_ratio(self):
        """CASA Ratio (Banking Specific)"""
        return pd.Series(np.nan, index=self.df.index)

    # --- Master Method ---

    def get_all_metrics(self, period_days=365, growth_lag=1):
        """Returns a DataFrame with all calculated metrics."""
        summary                       = pd.DataFrame(index=self.df.index)
        summary['EPS']                = self.calculate_eps()
        summary['EPS Growth %']       = self.calculate_eps_growth(periods=growth_lag)
        summary['EBIT']               = self.calculate_ebit()
        summary['ROCE %']             = self.calculate_roce()
        summary['ROE %']              = self.calculate_roe()
        summary['ROA %']              = self.calculate_roa()
        summary['D/E Ratio']          = self.calculate_de_ratio()
        summary['OPM %']              = self.calculate_opm()
        summary['CCC (Days)']         = self.calculate_ccc(period_days)
        summary['Capital Employed']   = self.calculate_capital_employed()
        summary['Shareholder Equity'] = self.calculate_shareholder_equity()

        # summary['P/E Ratio'] = self.calculate_pe_ratio()
        # summary['PEG Ratio'] = self.calculate_peg_ratio()

        return summary