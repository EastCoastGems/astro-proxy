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
        data = request.json()

        date_str = data.get('date')  # e.g., '1990-06-15'
        time_str = data.get('time')  # e.g., '14:30'
        lat = data.get('latitude')   # e.g., 40.7128
        lon = data.get('longitude')  # e.g., -74.0060

        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=lat, lng=lon)
        tz = pytz.timezone(timezone_str)

        dt_naive = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        dt_aware = tz.localize(dt_naive)
        ts = load.timescale()
        t = ts.from_datetime(dt_aware)

        observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
        sun_pos = observer.at(t).observe(sun).apparent().ecliptic_latlon()
        moon_pos = observer.at(t).observe(moon).apparent().ecliptic_latlon()

        sun_lon = sun_pos[1].degrees % 360
        moon_lon = moon_pos[1].degrees % 360

        zodiac = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                  "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

        def get_sign(degrees):
            return zodiac[int(degrees / 30)]

        result = {
            "sun": get_sign(sun_lon),
            "moon": get_sign(moon_lon),
            "datetime": dt_aware.isoformat(),
            "timezone": timezone_str
        }

        return {
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({ "error": str(e) })
        }
