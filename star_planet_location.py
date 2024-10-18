import streamlit as st

from skyfield.api import load, Topos
from datetime import datetime, timezone
import pytz
import plotly.graph_objs as go
import numpy as np
import swisseph as swe

st.set_page_config(layout="wide")

# Define Nakshatras with their starting degrees
nakshatras = [
    (0, 'Ashwini'), (13.3333333, 'Bharani'), (26.6666667, 'Krittika'),
    (40.0, 'Rohini'), (53.3333333, 'Mrigashira'), (66.6666667, 'Ardra'),
    (80.0, 'Punarvasu'), (93.3333333, 'Pushya'), (106.6666667, 'Ashlesha'),
    (120.0, 'Magha'), (133.3333333, 'Purva Phalguni'), (146.6666667, 'Uttara Phalguni'),
    (160.0, 'Hasta'), (173.3333333, 'Chitra'), (186.6666667, 'Swati'),
    (200.0, 'Vishakha'), (213.3333333, 'Anuradha'), (226.6666667, 'Jyeshtha'),
    (240.0, 'Mula'), (253.3333333, 'Purva Ashadha'), (266.6666667, 'Uttara Ashadha'),
    (280.0, 'Shravana'), (293.3333333, 'Dhanishta'), (306.6666667, 'Shatabhisha'),
    (320.0, 'Purva Bhadrapada'), (333.3333333, 'Uttara Bhadrapada'), (346.6666667, 'Revati')
]

# Define Rashis (Zodiac Signs) with their starting degrees
rashis = [
    (0, 'Aries'), (30, 'Taurus'), (60, 'Gemini'), (90, 'Cancer'),
    (120, 'Leo'), (150, 'Virgo'), (180, 'Libra'), (210, 'Scorpio'),
    (240, 'Sagittarius'), (270, 'Capricorn'), (300, 'Aquarius'), (330, 'Pisces')
]

# Set up the Streamlit interface
st.title("Planetary Positions: Sidereal and Tropical")

# Load ephemeris data
try:
    eph = load('de430_1850-2150.bsp')
except OSError:
    st.warning("Unable to load de430_1850-2150.bsp. Falling back to de421.bsp.")
    eph = load('de421.bsp')
planets = eph

moon = planets['moon']
sun = planets['sun']
earth = planets['earth']

# Include other planets
mercury = planets['mercury barycenter']
venus = planets['venus barycenter']
mars = planets['mars barycenter']
jupiter = planets['jupiter barycenter']
saturn = planets['saturn barycenter']

# Set location to Delhi
delhi = earth + Topos('28.6139 N', '77.2090 E')
delhi_tz = pytz.timezone('Asia/Kolkata')
ts = load.timescale()

# Functions to calculate Ayanamsa
def calculate_lahiri_ayanamsa(t):
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ayanamsa_value = swe.get_ayanamsa(t.tt)  # Using Terrestrial Time (tt) for accuracy
    return ayanamsa_value

def calculate_kp_ayanamsa(t):
    swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
    ayanamsa_value = swe.get_ayanamsa(t.tt)
    return ayanamsa_value

# Function to determine Nakshatra for a given degree
def get_nakshatra(degree):
    total_nakshatras = len(nakshatras)
    nakshatra_length = 360 / total_nakshatras  # Each nakshatra spans 360/27=13.333... degrees
    index = int(degree / nakshatra_length)
    index = index % total_nakshatras  # Ensure index is within range
    return nakshatras[index][1]  # Return the name of the nakshatra

# Function to determine Rashi for a given degree
def get_rashi(degree):
    total_rashis = len(rashis)
    rashi_length = 360 / total_rashis  # Each rashi spans 30 degrees
    index = int(degree / rashi_length)
    index = index % total_rashis  # Ensure index is within range
    return rashis[index][1]  # Return the name of the rashi

# Function to plot positions using Plotly
def plot_positions_plotly(bodies_positions, chart_width, chart_height, show_nakshatras, show_rashi_circle):
    fig = go.Figure()

    # Plot Rashis with color shading if required
    if show_rashi_circle:
        angles = np.linspace(0, 360, len(rashis) + 1)
        for idx in range(len(rashis)):
            start_angle = angles[idx]
            end_angle = angles[idx + 1]
            name = rashis[idx][1]
            fig.add_trace(go.Scatterpolar(
                r=[2.2, 2.0, 2.0, 2.2],
                theta=[start_angle, start_angle, end_angle, end_angle],
                fill='toself',
                mode='none',
                fillcolor=f'rgba({50 + idx * 10}, {100 + idx * 5}, {150 - idx * 5}, 0.1)',
                showlegend=False
            ))

            # Rashi boundary line
            fig.add_trace(go.Scatterpolar(
                r=[2.2, 0],
                theta=[start_angle, start_angle],
                mode='lines',
                line=dict(color='black', dash='dash'),
                showlegend=False
            ))

            # Rashi name label
            fig.add_trace(go.Scatterpolar(
                r=[2.4],
                theta=[(start_angle + end_angle) / 2],
                mode='text',
                text=[f"{name}"],
                textposition='top center',
                showlegend=False
            ))

    # Plot Nakshatras with color shading if required
    if show_nakshatras:
        angles = np.linspace(0, 360, len(nakshatras) + 1)
        for idx in range(len(nakshatras)):
            start_angle = angles[idx]
            end_angle = angles[idx + 1]
            name = nakshatras[idx][1]
            fig.add_trace(go.Scatterpolar(
                r=[2.0, 0, 0, 2.0],
                theta=[start_angle, start_angle, end_angle, end_angle],
                fill='toself',
                mode='none',
                fillcolor=f'rgba({100 + idx * 5}, {150 + idx * 3}, {200 - idx * 4}, 0.1)',
                showlegend=False
            ))

            # Nakshatra boundary line
            fig.add_trace(go.Scatterpolar(
                r=[2.0, 0],
                theta=[start_angle, start_angle],
                mode='lines',
                line=dict(color='gray', dash='dot'),
                showlegend=False
            ))

            # Nakshatra name label
            fig.add_trace(go.Scatterpolar(
                r=[2.1],
                theta=[(start_angle + end_angle) / 2],
                mode='text',
                text=[f"{name}"],
                textposition='top center',
                showlegend=False
            ))

    # Plot positions of celestial bodies
    for body_name, data in bodies_positions.items():
        fig.add_trace(go.Scatterpolar(
            r=[data['radius']],
            theta=[data['degree']],
            mode='markers+text',
            marker=dict(size=12, color=data['color']),
            text=[f"{body_name}\n{data['degree']:.2f}°\n{data.get('nakshatra', '')}"],
            textposition='bottom center',
            name=body_name
        ))

    fig.update_layout(
        width=chart_width,
        height=chart_height,
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 2.5]),
            angularaxis=dict(rotation=90, direction="counterclockwise")
        ),
        showlegend=True,
        title=f"Astrological Chart"
    )

    return fig

# Main logic
current_time = datetime.now(delhi_tz)
t = ts.from_datetime(current_time.astimezone(timezone.utc))

# Select Coordinate System option
coord_option = st.selectbox("Select Coordinate System", options=["Sidereal", "Tropical", "Both"], index=0)

# Initialize ayanamsa_option to avoid NameError
ayanamsa_option = None

# Select Ayanamsa option (only relevant for Sidereal or Both)
if coord_option in ["Sidereal", "Both"]:
    ayanamsa_option = st.selectbox("Select Ayanamsa", options=["My_ayanamsa", "KP", "Lahiri", "Custom"], index=0)

    if ayanamsa_option == 'Custom':
        custom_ayanamsa = st.number_input("Enter custom ayanamsa in degrees", value=0.0, step=0.01)
    else:
        custom_ayanamsa = None

    # Calculate Ayanamsa based on selected option
    if ayanamsa_option == 'My_ayanamsa':
        ayanamsa = 27.85
        swe.set_sid_mode(swe.SIDM_USER, ayanamsa)
    elif ayanamsa_option == 'KP':
        ayanamsa = calculate_kp_ayanamsa(t)
    elif ayanamsa_option == 'Lahiri':
        ayanamsa = calculate_lahiri_ayanamsa(t)
    elif ayanamsa_option == 'Custom':
        ayanamsa = custom_ayanamsa
        swe.set_sid_mode(swe.SIDM_USER, ayanamsa)
    else:
        ayanamsa = 0.0
else:
    ayanamsa = 0.0  # Not used in Tropical calculations

# Allow user to toggle Rashi circle
show_rashi_circle = st.checkbox("Show Rashi (Zodiac Signs) Circle", value=True)

# List of celestial bodies to include
celestial_bodies = {
    'Sun': {'object': sun, 'color': 'orange', 'radius': 1.3},
    'Moon': {'object': moon, 'color': 'blue', 'radius': 1.4},
    'Mercury': {'object': mercury, 'color': 'green', 'radius': 1.5},
    'Venus': {'object': venus, 'color': 'pink', 'radius': 1.6},
    'Mars': {'object': mars, 'color': 'red', 'radius': 1.7},
    'Jupiter': {'object': jupiter, 'color': 'purple', 'radius': 1.8},
    'Saturn': {'object': saturn, 'color': 'brown', 'radius': 1.9}
}

# Calculate positions
bodies_positions = {}

for body_name, body_info in celestial_bodies.items():
    astrometric = delhi.at(t).observe(body_info['object'])
    apparent = astrometric.apparent()
    _, lon, _ = apparent.ecliptic_latlon()
    tropical_degree = lon.degrees % 360
    if coord_option == "Tropical":
        degree = tropical_degree
        nakshatra = get_nakshatra(degree) if body_name != 'Sun' else ''
    elif coord_option == "Sidereal":
        degree = (tropical_degree - ayanamsa) % 360
        nakshatra = get_nakshatra(degree)
    else:  # Both
        degree = (tropical_degree - ayanamsa) % 360
        nakshatra = get_nakshatra(degree)
        # Store tropical positions separately
        bodies_positions[f"{body_name} (Tropical)"] = {
            'degree': tropical_degree,
            'nakshatra': '',
            'color': body_info['color'],
            'radius': body_info['radius'] - 0.1
        }
    bodies_positions[body_name] = {
        'degree': degree,
        'nakshatra': nakshatra,
        'color': body_info['color'],
        'radius': body_info['radius']
    }

# Function to calculate Rahu and Ketu positions
def calculate_lunar_nodes(current_time, ayanamsa, coord_option):
    # Convert current time to UTC
    current_time_utc = current_time.astimezone(timezone.utc)
    # Convert current time to Julian Day
    jd = swe.julday(current_time_utc.year, current_time_utc.month, current_time_utc.day,
                    current_time_utc.hour + current_time_utc.minute / 60 + current_time_utc.second / 3600)

    # Calculate Rahu (mean node) in tropical zodiac
    flags = swe.FLG_SWIEPH  # Use Swiss Ephemeris
    rahu_info = swe.calc_ut(jd, swe.MEAN_NODE, flags)
    rahu_tropical = rahu_info[0][0] % 360  # value fecthed from tuple 

    if coord_option == "Sidereal" or coord_option == "Both":
        # Adjust for ayanamsa
        rahu_degree = (rahu_tropical - ayanamsa) % 360
    else:
        rahu_degree = rahu_tropical

    # Ketu is opposite Rahu
    ketu_degree = (rahu_degree + 180) % 360

    rahu_nakshatra = get_nakshatra(rahu_degree)
    ketu_nakshatra = get_nakshatra(ketu_degree)

    return {
        'Rahu': {'degree': rahu_degree, 'nakshatra': rahu_nakshatra, 'color': 'black', 'radius': 2.0},
        'Ketu': {'degree': ketu_degree, 'nakshatra': ketu_nakshatra, 'color': 'gray', 'radius': 2.1}
    }

# Add Rahu and Ketu positions
lunar_nodes = calculate_lunar_nodes(current_time, ayanamsa, coord_option)
bodies_positions.update(lunar_nodes)

# Display current degrees and nakshatras
st.subheader("Current Positions")
for body_name, data in bodies_positions.items():
    if 'Tropical' in body_name:
        st.write(f"**{body_name}:** {data['degree']:.2f}°, Rashi: {get_rashi(data['degree'])}")
    else:
        st.write(f"**{body_name}:** {data['degree']:.2f}°, Nakshatra: {data.get('nakshatra', '')}, Rashi: {get_rashi(data['degree'])}")

# Input slider for chart size adjustment
chart_width = st.slider("Adjust Chart Width", min_value=600, max_value=1600, value=1200, step=100)
chart_height = st.slider("Adjust Chart Height", min_value=400, max_value=1200, value=1000, step=100)

# Determine whether to show Nakshatras on the plot
show_nakshatras = coord_option in ["Sidereal", "Both"]

# Display the plot using Plotly
fig = plot_positions_plotly(bodies_positions, chart_width, chart_height, show_nakshatras, show_rashi_circle)
st.plotly_chart(fig, use_container_width=True)
