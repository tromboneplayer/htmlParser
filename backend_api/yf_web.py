import requests
import re
import json
import yfinance as yf
from bs4 import BeautifulSoup 
from utilities.util import fix_unprintable
from configs.config import YAHOO_URL_PROFILE, USER_AGENT, USE_YF_LIBRARY, NOT_AVAILABLE


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
    '''Parse the Yahoo Finance stock page so we can retrieve the json data.'''
    
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


def get_company_profile_web_api(symbol: str) -> dict:
    '''Given a symbol, use the Yahoo Finance website or API to retrieve company profile information.  This includes the sector and industry data.'''
    
    if not symbol:
        msg = f"get_company_profile_web_api: Exception reading company profile data. No symbol provided."
        raise Exception(msg)
        
    print(f"getting data for {symbol}")

    if USE_YF_LIBRARY:
        return _get_company_profile_library(symbol)
    else:
        return _get_company_profile_web(symbol)


def _get_company_profile_web(symbol: str) -> dict:
    '''Get the company profile data using the Yahoo Finance website.'''
        
    webpage = _get_webpage(symbol)
    
    if not webpage:
        return (symbol, NOT_AVAILABLE, NOT_AVAILABLE)
    
    company_profile = _parse_stock_page_YF(webpage)
    
    if not company_profile:
        return {"symbol": symbol, "sector":NOT_AVAILABLE, "industry":NOT_AVAILABLE}
    
    try:
        sector = company_profile["sector"]
        industry = company_profile["industry"]
        industry = fix_unprintable(industry)
        return {"symbol": symbol, "sector":sector, "industry":industry}
    except KeyError as e:
        return {"symbol": symbol, "sector":NOT_AVAILABLE, "industry":NOT_AVAILABLE}
    except Exception as e:
        print(f"_get_company_profile_web: Exception reading company profile data {e}")
        raise e


def _get_company_profile_library(symbol: str) -> dict:
    '''Get the company profile data using the Yahoo Finance python library.  This is slower than the web method, but an easier implementation.'''
    
    company_profile = yf.Ticker(symbol)

    if not company_profile:
        return {"symbol": symbol, "sector":NOT_AVAILABLE, "industry":NOT_AVAILABLE}

    try:
        sector = company_profile.info["sector"]
        industry = company_profile.info["industry"]
        industry = fix_unprintable(industry)
        return {"symbol": symbol, "sector":sector, "industry":industry}
    except KeyError as e:
        return {"symbol": symbol, "sector":NOT_AVAILABLE, "industry":NOT_AVAILABLE}
    except Exception as e:
        msg = f"_get_company_profile_library: Exception reading company profile data {e}"
        print(msg)
        raise e