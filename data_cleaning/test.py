import pandas as pd
import numpy as np
def get_df():
    df = pd.read_csv('compustat.csv')
    df_with_ratios = pd.DataFrame(df[['datadate', 'gvkey', 'fqtr', 'fyr', 'tic', 'sic']])
    df_with_ratios.drop(['fqtr', 'fyr'], axis=1, inplace=True)
    df_with_ratios['ta'] = df['atq']
    df_with_ratios['lt'] = df['ltq']
    df_with_ratios['dlc'] = df['dlcq']
    df_with_ratios['dtp'] = df['txditcq']
    df_with_ratios['che'] = df['cheq']
    df_with_ratios['lct'] = df['lctq']
    df_with_ratios['act'] = df['atq']
    df_with_ratios['invtq'] = df['invtq']
    df_with_ratios['intanq'] = df['intanq']
    df_with_ratios['oiadp'] = df['oibdpq'] / df['oibdpy']
    df_with_ratios['txp'] = df['txpq']
    # df_with_ratios['xint'] = df['tieq'] / df['tiey']
    df_with_ratios['pi'] = df['piq'] / df['piy']
    df_with_ratios['ni'] = df['niq'] / df['niy']
    df_with_ratios['rev'] = df['revtq'] / df['revty']
    df_with_ratios['cogs'] = df['cogsq'] / df['cogsy']
    df_with_ratios['oancf'] = df['oancfy']
    df_with_ratios['ivncf'] = df['ivncfy']
    df_with_ratios['fncfa'] = df['fincfy']
    df_with_ratios['curr_ratio'] = df['actq'] / df['lctq']
    df_with_ratios['quick_ratio'] = (df['actq'] - df['invtq']) / df['lctq']
    df_with_ratios['cash_ratio'] = df['chechy'] / df['lctq']
    df_with_ratios['net_working_capital'] = df['actq'] - df['lctq']
    df_with_ratios['debt_ratio'] = df['dlttq'] / df['actq']
    df_with_ratios['debt_equity_ratio'] = df['dlttq'] / df['ceqq']
    df_with_ratios['equity_ratio'] = df['ceqq'] / df['actq']
    df_with_ratios['financial_leverage_ratio'] = df['actq'] / df['ceqq']
    # df_with_ratios['interest_coverage_ratio'] = (df['uopiq'] + df['dpq']) / df['tiey']
    df_with_ratios['cashflow_debt_ratio'] = df['oancfy'] / df['dlttq']
    df_with_ratios['net_profit_margin'] = 100 * (df['revtq'] - df['cogsq']) / df['revtq']
    df_with_ratios['roa'] = (df['niq'] / df['atq']) * 100
    df_with_ratios['asset_turnover'] = df['saleq'] / df['saley']
    df_with_ratios['inventory_turnover'] = df['invchy']
    df_with_ratios['inventory_days'] = df_with_ratios['inventory_turnover']
    df_with_ratios['receivables_turnover'] = df['saleq'] / df['rectq']
    df_with_ratios['dso'] = 365 / df_with_ratios['receivables_turnover']
    df_with_ratios['working_capital_turnover'] = df['saleq'] / df['wcapq']
    # df_with_ratios['debt_service_coverage_ratio'] = df['uopiq'] / df['dlttq']
    # df_with_ratios['cash_coverage_ratio'] = df['oibdpq'] / df['tieq']
    df_with_ratios['pe_ratio'] = df['prccq'] / df['epsf12']
    # df_with_ratios['pb_ratio'] = df['prccq'] / (df['uceqq'] / df['cshoq'])
    # df_with_ratios['div_payout_ratio'] = df['dvy'] / ((df['uniamiq'] * 100) / df['saley'])
    df_with_ratios['retention_ratio'] = df['req'] / df_with_ratios['ni']
    # df_with_ratios['ebitda'] = (df['uopiq'] + df['dpq'] * 100) / df['revtq']

    df_with_ratios['datadate'] = pd.to_datetime(df_with_ratios['datadate'])
    df_with_ratios['year'] = df_with_ratios['datadate'].dt.year
    df_with_ratios['quarter'] = df_with_ratios['datadate'].dt.quarter
    df_with_ratios = df_with_ratios.drop_duplicates(subset=['gvkey', 'year', 'quarter'])
    df_drop_gvkey = df_with_ratios.drop(['sic', 'tic', 'year', 'quarter', 'datadate'], axis=1)
    df_drop_gvkey = df_drop_gvkey.groupby('gvkey').apply(lambda group: group.iloc[:, 1:].isna().all().all())
    to_drop = df_drop_gvkey[df_drop_gvkey == True]
    gvkeys_to_drop = list(to_drop.index)
    df_with_ratios_dropped_gvkey = df_with_ratios[~df_with_ratios['gvkey'].isin(gvkeys_to_drop)]
    cols_df = df_with_ratios_dropped_gvkey.drop(['gvkey', 'sic', 'tic', 'year', 'quarter', 'datadate'], axis=1)
    all_na_rows = cols_df[cols_df.isna().all(axis=1)]
    df_with_nans = df_with_ratios_dropped_gvkey.loc[all_na_rows.index]
    df_with_nans_counts = df_with_nans.groupby('gvkey').size()
    gvkey_with_bad_data = df_with_nans_counts[df_with_nans_counts > 10]
    df_with_ratios_dropped_gvkey_v2 = df_with_ratios_dropped_gvkey[
        ~df_with_ratios_dropped_gvkey['gvkey'].isin(gvkey_with_bad_data.index)]

    return df_with_ratios_dropped_gvkey_v2


def inpute():
    df_with_ratios_dropped_gvkey_v2 = get_df()
    sector_date_median = df_with_ratios_dropped_gvkey_v2.groupby(['sic', 'year', 'quarter']).median()
    cols_to_check = [col for col in df_with_ratios_dropped_gvkey_v2.columns if
                     col not in ['datadate', 'year', 'quarter', 'sic', 'gvkey', 'tic']]
    df_to_inpute = df_with_ratios_dropped_gvkey_v2[df_with_ratios_dropped_gvkey_v2.isna().any(axis=1)]
    df_inputed = df_with_ratios_dropped_gvkey_v2.copy()
    df_to_inpute['Index'] = df_to_inpute.index
    print("Starting..................")
    for row in df_to_inpute.to_dict('records'):
        index = row['Index']
        sic = row['sic']
        year = row['year']
        quarter = row['quarter']
        print(index)
        for col in cols_to_check:
            value = row[col]
            if np.isnan(value):
                median = sector_date_median[sector_date_median.index == (sic, year, quarter)][col].iloc[0]
                df_inputed.at[index, col] = median
    df_inputed.to_csv('df_inputed.csv')


