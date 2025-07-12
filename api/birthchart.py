from http.server import BaseHTTPRequestHandler
import json
from skyfield.api import load, Topos
from skyfield.api import N, W, wgs84
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz

# Load ephemeris data
planets = load('de421.bsp')
earth = planets['earth']
sun = planets['sun']
moon = planets['moon']

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        date_str = data.get('date')  # e.g., '1990-06-15'
        time_str = data.get('time')  # e.g., '14:30'
        lat = data.get('latitude')   # e.g., 40.7128
        lon = data.get('longitude')  # e.g., -74.0060

        # Find timezone
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=lat, lng=lon)
        tz = pytz.timezone(timezone_str)

        # Convert to datetime with timezone
        dt_naive = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        dt_aware = tz.localize(dt_naive)
        ts = load.timescale()
        t = ts.from_datetime(dt_aware)

        # Observer position
        observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)

        # Sun and Moon positions
        sun_pos = observer.at(t).observe(sun).apparent().ecliptic_latlon()
        moon_pos = observer.at(t).observe(moon).apparent().ecliptic_latlon()

        sun_lon = sun_pos[1].degrees % 360
        moon_lon = moon_pos[1].degrees % 360

        # Get signs
        zodiac = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                  "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

        def get_sign(degrees):
            return zodiac[int(degrees / 30)]

        sun_sign = get_sign(sun_lon)
        moon_sign = get_sign(moon_lon)

        result = {
            "sun": sun_sign,
            "moon": moon_sign,
            "datetime": dt_aware.isoformat(),
            "timezone": timezone_str
        }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
