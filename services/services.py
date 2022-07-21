from backend_api.yf_web import get_company_profile


def process_file(symbols_file):
    output_data = list()
    
    for symbol in symbols_file:
        symbol = symbol.strip()
        symbol_data = get_company_profile(symbol)

        output_data.append(symbol_data)
    
    return output_data