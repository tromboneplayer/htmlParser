import requests
import re
import json
import yfinance as yf
from bs4 import BeautifulSoup 
from utilities.util import fix_unprintable
from configs.config import YAHOO_URL_PROFILE, USER_AGENT, USE_YF_LIBRARY


def _get_webpage(symbol):
    
    try:
        url = YAHOO_URL_PROFILE.format(s=symbol)
        webpage = requests.get(url, headers={"User-Agent": USER_AGENT})
        if webpage.status_code == 200:
            return webpage
        else:
            msg = f"_get_webpage: Page get error: {webpage.status_code}"
            print(msg)
            raise Exception(msg)
    except Exception as e:
        print(f"_get_webpage: Page not found for {symbol}")
        return None


def _parse_stock_page_YF(webpage):
    
    soup = BeautifulSoup(webpage.content, 'html.parser', from_encoding='utf-8')
    
    pattern = re.compile(r'\s--\sData\s--\s') #raw string
    
    try:
        script_data = soup.find('script', text=pattern).contents[0]
        start = script_data.find("context")-2
        json_data = json.loads(script_data[start:-12])
        asset_profile = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile']
        # summary_detail = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']
    except KeyError as e:
        asset_profile = None
    except Exception as e:
        print(f"_parse_stock_page_YF: Error parsing Yahoo Finance data. Exception {e}")
        raise e

    return asset_profile


def get_company_profile(symbol: str) -> tuple:
    
    print(f"getting data for {symbol}")

    if USE_YF_LIBRARY:
        return _get_company_profile_library(symbol)
    else:
        return _get_company_profile_web(symbol)


def _get_company_profile_web(symbol: str) -> tuple:
    '''Get the company profile data using the Yahoo Finance website.'''
        
    webpage = _get_webpage(symbol)
    
    if not webpage:
        sector = "n/a"
        industry = "n/a"
        return (symbol, sector, industry)
    
    company_profile = _parse_stock_page_YF(webpage)
    
    if not company_profile:
        sector = "n/a"
        industry = "n/a"
        return (symbol, sector, industry)
    
    try:
        sector = company_profile["sector"]
        industry = company_profile["industry"]
        industry = fix_unprintable(industry)
        return (symbol, sector, industry)
    except KeyError as e:
        return (symbol, "n/a", "n/a")
    except Exception as e:
        print(f"_get_company_profile_web: Exception reading company profile data {e}")
        raise e


def _get_company_profile_library(symbol: str) -> tuple:
    '''Get the company profile data using the Yahoo Finance python library.  This is slower than the web method, but an easier implementation.'''
    
    symbol_data = yf.Ticker(symbol)

    try:
        sector = symbol_data.info["sector"]
        industry = symbol_data.info["industry"]
        industry = fix_unprintable(industry)
        return (symbol, sector, industry)
    except KeyError as e:
        return (symbol, "n/a", "n/a")
    except Exception as e:
        msg = f"_get_company_profile_library: Exception reading company profile data {e}"
        print(msg)
        raise e