from skyfield.api import load, Topos
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz
import json

def handler(request):
    try:
        data = request.json()

        date_str = data.get('date')
        time_str = data.get('time')
        lat = data.get('latitude')
        lon = data.get('longitude')

        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=lat, lng=lon)
        tz = pytz.timezone(timezone_str)

        dt_naive = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        dt_aware = tz.localize(dt_naive)
        ts = load.timescale()
        t = ts.from_datetime(dt_aware)

        planets = load('de421.bsp')
        earth = planets['earth']
        sun = planets['sun']
        moon = planets['moon']
        observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)

        sun_pos = observer.at(t).observe(sun).apparent().ecliptic_latlon()
        moon_pos = observer.at(t).observe(moon).apparent().ecliptic_latlon()

        sun_lon = sun_pos[1].degrees % 360
        moon_lon = moon_pos[1].degrees % 360

        zodiac = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                  "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        get_sign = lambda deg: zodiac[int(deg / 30)]

        return {
            "statusCode": 200,
            "body": json.dumps({
                "sun": get_sign(sun_lon),
                "moon": get_sign(moon_lon),
                "datetime": dt_aware.isoformat(),
                "timezone": timezone_str
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }
