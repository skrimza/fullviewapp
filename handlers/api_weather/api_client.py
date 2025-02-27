import requests
from config import SETTINGS

class ApiClient:
    key = SETTINGS.API_KEY.get_secret_value()
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    
    def get_weather_data(self):
        get_weather = requests.get(
            url=self.base_url,
            params={
                "key": self.key,
                "q": "46.216.41.123",
                "days": 4
            }
        )
        return get_weather.json()


