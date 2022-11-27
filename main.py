from finviz import read_stock_info, read_tickers_parallel, save_data_to_file, load_data_from_file

def filter_func(stock):
    dividend = stock['Dividend %'] != '-' and float(stock['Dividend %'].strip('%')) >= 3.00
    debt = stock['Debt/Eq'] != '-' and float(stock['Debt/Eq']) <= 0.60
    pe_ratio = stock['P/E'] != '-' and float(stock['P/E']) <= 2.0

    return dividend and debt and pe_ratio

def main():
    company_data = load_data_from_file('company_data')
    
    f = filter(filter_func, company_data)
    filtered_company_data = list(f)

    for entry in filtered_company_data:
        print(f"\n{entry}\n")

    print(f"Found {len(filtered_company_data)} companies matching criteria")
    print(f"Tickers: {', '.join(list(map(lambda x : x['STOCK_TICKER'], filtered_company_data)))}")

if __name__ == "__main__":
    main()
