'''Client API app that asks the user for longitude and latitude, the gets the values of the parameters office, gridX, and gridY
in order to call the forecast API and get the forecast data for the given location.'''

import requests


def get_location():
    """
    Get the location from the user.
    Returns:
        tuple: A tuple containing the latitude and longitude of the location.
    """
    while True:
        try:
            print("Please enter the latitude and longitude of the location.")
            print("Coordinates should be in decimal form.")
            print("Example: 38.8977, -77.0365 (White House)")
            lat = float(input("Enter latitude: "))
            lon = float(input("Enter longitude: "))
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return lat, lon
            else:
                print("Invalid coordinates. Please enter valid latitude and longitude.")
        except ValueError:
            print("Invalid input. Please enter numeric values for latitude and longitude.")

def get_grid_info(lat, lon):
    """
    Get the grid information for the given latitude and longitude.
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
    Returns:
        tuple: A tuple containing the office, gridX, and gridY values.
    """
    # API call to get grid information
    url = f"https://api.weather.gov/points/{lat},{lon}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        office = data['properties']['gridId']
        gridX = data['properties']['gridX']
        gridY = data['properties']['gridY']
        return office, gridX, gridY
    except requests.exceptions.RequestException as e:
        print(f"Error fetching grid information: {e}")
        return None, None, None
    except KeyError:
        print("Error parsing grid information. Please try again.")
        return None, None, None
    
def forecast(office, gridX, gridY):
    """
    Get the forecast data for the given office, gridX, and gridY values.
    Args:
        office (str): The office code.
        gridX (int): The grid X value.
        gridY (int): The grid Y value.
    Returns:
        str: The forecast data in a user-friendly format.
    """
    # API call to get forecast data
    url = f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        forecast_data = data['properties']['periods']
        forecast_str = "Forecast:\n"
        for period in forecast_data:
            forecast_str += f"{period['name']}: {period['shortForecast']} with a temperature of {period['temperature']} F\n"
        return forecast_str
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forecast data: {e}")
        return None
    except KeyError:
        print("Error parsing forecast data. Please try again.")
        return None

def main():
    """
    Main function to run the NOAA forecast client.
    """
    print("Welcome to the NOAA Forecast Client!")
    lat, lon = get_location()
    office, gridX, gridY = get_grid_info(lat, lon)
    
    if office is not None and gridX is not None and gridY is not None:
        forecast_data = forecast(office, gridX, gridY)
        if forecast_data:
            print(forecast_data)
        else:
            print("Failed to retrieve forecast data.")
    else:
        print("Failed to retrieve grid information.")

if __name__ == "__main__":
    main()