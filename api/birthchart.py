#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler
import json
from skyfield.api import load, Topos
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz

# Load ephemeris data
planets = load('de421.bsp')
earth = planets['earth']
sun = planets['sun']
moon = planets['moon']

zodiac = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def get_sign(degrees):
    return zodiac[int(degrees / 30)]

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

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

        observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)

        sun_pos = observer.at(t).observe(sun).apparent().ecliptic_latlon()
        moon_pos = observer.at(t).observe(moon).apparent().ecliptic_latlon()

        sun_lon =_
