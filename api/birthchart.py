from http.server import BaseHTTPRequestHandler
import json

from skyfield.api import load, Topos
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read and parse the JSON body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            # Extract fields from input
            birth_date = data.get("date")        # Format: "YYYY-MM-DD"
            birth_time = data.get("time")        # Format: "HH:MM"
            latitude = float(data.get("latitude"))
            longitude = float(data.get("longitude"))

            # Determine timezone
            tf = TimezoneFinder()
            tz_str = tf.timezone_at(lng=longitude, lat=latitude)
            if not tz_str:
                raise ValueError("Could not determine timezone for coordinates")

            # Convert to UTC datetime
            local_tz = pytz.timezone(tz_str)
            local_dt = local_tz.localize(datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M"))
            utc_dt = local_dt.astimezone(pytz.utc)

            # Load ephemeris and create chart data (basic demo)
            eph = load('de421.bsp')
            ts = load.timescale()
            t = ts.from_datetime(utc_dt)

            planets = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn']
            positions = {}

            for planet in planets:
                body = getattr(eph, planet)
                astrometric = body.at(t).observe(Topos(latitude_degrees=latitude, longitude_degrees=longitude))
                alt, az, distance = astrometric.apparent().altaz()
                positions[planet] = {
                    "altitude_degrees": alt.degrees,
                    "azimuth_degrees": az.degrees
                }

            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "datetime_utc": utc_dt.isoformat(),
                "positions": positions
            }).encode())

        except Exception as e:
            # Error response
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            error = {"error": str(e)}
            self.wfile.write(json.dumps(error).encode())
