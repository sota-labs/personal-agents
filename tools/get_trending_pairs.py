import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import requests
from config import settings

def get_trending_pairs(jwt_token: str = "", resolution: str = "5m", limit: int = 5) -> dict:
    """
    Get a list of trending trading pairs
    
    Args:
        resolution (str): Time frame (default: "5m")
        limit (int): Maximum number of pairs to return (default: 5)
        
    Returns:
        dict: Dictionary containing list of trading pairs with information:
            - pairs (list): List of trading pairs:
                - pairId (str): ID of the trading pair
                - dex (str): Name of the exchange
                - tokenBase (dict): Base token information
                    - address (str): Token contract address
                    - name (str): Token name
                    - symbol (str): Token symbol
                    - priceUsd (float): Token price in USD
                - liquidityUsd (float): Liquidity in USD
                - volumeUsd (float): Trading volume in USD
                - priceChange (dict): Price change percentages for different timeframes
                    - 5m (float): 5-minute change
                    - 1h (float): 1-hour change
                    - 6h (float): 6-hour change
                    - 24h (float): 24-hour change
    """
    try:
        url = f"{settings.raiden.api_common_url}/api/v1/sui/pairs/trending"
        
        params = {
            "page": 1,
            "limit": limit,
            "resolution": resolution,
            "network": "sui"
        }
        
        headers = {
            "accept": "application/json"
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            pairs = []
            
            for pair in data:
                pairs.append({
                    # 'pairId': pair.get('pairId'),
                    # 'dex': pair.get('dex', {}).get('name'),
                    'tokenBase': {
                        'address': pair.get('tokenBase', {}).get('address'),
                        'name': pair.get('tokenBase', {}).get('name'),
                        'symbol': pair.get('tokenBase', {}).get('symbol'),
                        'priceUsd': float(pair.get('tokenBase', {}).get('priceUsd', 0))
                    },
                    'liquidityUsd': float(pair.get('liquidityUsd', 0)),
                    'volumeUsd': float(pair.get('volumeUsd', 0)),
                    'priceChange': {
                        '5m': pair.get('stats', {}).get('percent', {}).get('5m', 0),
                        '1h': pair.get('stats', {}).get('percent', {}).get('1h', 0),
                        '6h': pair.get('stats', {}).get('percent', {}).get('6h', 0),
                        '24h': pair.get('stats', {}).get('percent', {}).get('24h', 0)
                    }
                })
                
            return {'pairs': pairs}
        else:
            raise Exception(f"Error fetching trending pairs: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"API connection error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unknown error: {str(e)}")
    
    
# print(get_trending_pairs())