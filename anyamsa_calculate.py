from skyfield.api import load, Topos
from datetime import datetime
import pytz

# Function to convert degree, minute, second to decimal degrees
def dms_to_decimal(degree, minute, second):
    return degree + (minute / 60.0) + (second / 3600.0)

# Function to convert sign and degree to absolute degree
def sign_to_degree(sign, degree, minute, second):
    signs = {
        'Aries': 0, 'Taurus': 30, 'Gemini': 60, 'Cancer': 90, 'Leo': 120, 'Virgo': 150,
        'Libra': 180, 'Scorpio': 210, 'Sagittarius': 240, 'Capricorn': 270, 'Aquarius': 300, 'Pisces': 330
    }
    base_degree = signs[sign]
    return base_degree + dms_to_decimal(degree, minute, second)

# Input Moon sign and degree in KP astrology
kp_moon_sign = 'Pisces'  # Example: Pisces
kp_moon_deg_dms = (13, 49, 17)  # Format (degrees, minutes, seconds)

# Convert Moon degree from KP astrology to decimal degrees
sidereal_moon_degree = sign_to_degree(kp_moon_sign, *kp_moon_deg_dms)

# Load ephemeris data
eph = load('de430_1850-2150.bsp')
moon = eph['moon']
earth = eph['earth']

# Set location to Delhi
delhi = earth + Topos('28.6139 N', '77.2090 E')
delhi_tz = pytz.timezone('Asia/Kolkata')
ts = load.timescale()

# Calculate current Moon position
current_time = datetime.now(delhi_tz)
t = ts.utc(current_time.year, current_time.month, current_time.day,
           current_time.hour, current_time.minute, current_time.second)

astrometric_moon = delhi.at(t).observe(moon)
apparent_moon = astrometric_moon.apparent()
_, moon_lon, _ = apparent_moon.ecliptic_latlon()

# Calculate Ayanamsa (difference between tropical and sidereal positions)
ayanamsa_calculated = (moon_lon.degrees - sidereal_moon_degree) % 360

# Print results
print(f"Current Tropical Moon Degree: {moon_lon.degrees:.2f}°")
print(f"KP Sidereal Moon Degree: {sidereal_moon_degree:.2f}°")
print(f"Calculated Ayanamsa: {ayanamsa_calculated:.2f}°")
# Streamlit version below
# import streamlit as st
# from skyfield.api import load, Topos
# from datetime import datetime
# import pytz
# import numpy as np
#
# # Set up the Streamlit interface
# st.set_page_config(layout="wide")
# st.title("Calculate Ayanamsa")
#
# # Load ephemeris data
# try:
#     eph = load('de430_1850-2150.bsp')
# except OSError:
#     st.warning("Unable to load de430_1850-2150.bsp. Falling back to de421.bsp.")
#     eph = load('de421.bsp')
#
# moon = eph['moon']
# earth = eph['earth']
#
# # Set location to Delhi
# delhi = earth + Topos('28.6139 N', '77.2090 E')
# delhi_tz = pytz.timezone('Asia/Kolkata')
# ts = load.timescale()
#
# # Calculate current Moon position
# current_time = datetime.now(delhi_tz)
# t = ts.utc(current_time.year, current_time.month, current_time.day,
#            current_time.hour, current_time.minute, current_time.second)
#
# astrometric_moon = delhi.at(t).observe(moon)
# apparent_moon = astrometric_moon.apparent()
# _, moon_lon, _ = apparent_moon.ecliptic_latlon()
#
# # Input current Moon sidereal degree
# sidereal_moon_input = st.number_input("Enter current sidereal Moon degree (°)", value=0.0, step=0.01)
#
# # Calculate Ayanamsa from input
# if sidereal_moon_input:
#     ayanamsa_calculated = (moon_lon.degrees - sidereal_moon_input) % 360
#     st.write(f"**Calculated Ayanamsa:** {ayanamsa_calculated:.2f}°")
