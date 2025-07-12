import json
from skyfield.api import load, Topos
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz

planets = load('de421.bsp')
earth = planets['earth']
sun = planets['sun']
moon = planets['moon']

def handler(request):
    try:
        data = request.json

        # Extract input
        date_str = data.get("date")       # e.g., "1990-06-15"
        time_str = data.get("time")       # e.g., "14:30"
        lat = float(data.get("latitude")) # e.g., 40.7128
        lon = float(data.get("longitude"))# e.g., -74.0060

        if not (date_str and time_str and lat and lon):
            raise ValueError("Missing required fields.")

        # Find timezone from lat/lon
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=lat, lng=lon)
        if not timezone_str:
            raise ValueError("Could not determine timezone.")
        
        tz = pytz.timezone(timezone_str)
        dt_naive = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        dt = tz.localize(dt_naive)

        # Compute skyfield position
        ts = load.timescale()
        t = ts.from_datetime(dt)

        location = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
        astrometric_sun = location.at(t).observe(sun).apparent()
        astrometric_moon = location.at(t).observe(moon).apparent()

        sun_alt, sun_az, _ = astrometric_sun.altaz()
        moon_alt, moon_az, _ = astrometric_moon.altaz()

        result = {
            "datetime": dt.isoformat(),
            "timezone": timezone_str,
            "sun": {
                "altitude_degrees": sun_alt.degrees,
                "azimuth_degrees": sun_az.degrees
            },
            "moon": {
                "altitude_degrees": moon_alt.degrees,
                "azimuth_degrees": moon_az.degrees
            }
        }

        return {
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({"error": str(e)})
        }
