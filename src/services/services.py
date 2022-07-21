from backend_api.yf_data_api import get_company_profile_web_api


def process_file(symbols_file):
    output_data = list()
    
    for symbol in symbols_file:
        symbol = symbol.strip()
        symbol_data = get_company_profile_web_api(symbol)
        output_data.append(symbol_data)
    
    return output_data