# pip install streamlit
# pip install streamlit-folium
# cd Documents\Python_Scripts
# streamlit run wifi_streamlit_app.py

import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium


st.title('Checkpoint 2')

# Afficher un élément : st.write
st.title("Bornes wifi de la ville de Toulouse")

link = 'https://data.toulouse-metropole.fr/explore/dataset/bornes-wi-fi/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B'
df_borne = pd.read_csv(link, sep = ';')

def transfo(coord):
  latlon = coord.split(",")
  lat = float(latlon[0])
  lon = float(latlon[1])
  return [lat, lon]

df_borne['coordonnee']=""
df_borne['coordonnee'] = df_borne["Geo Point"].apply(transfo)

df_borne2 = df_borne.loc[:, ['site', 'coordonnee', 'zone_emission']]

# checkbox pour visualiser ou non le dataset (partie droite)
checkbox = st.checkbox("Show Dataset")
print(checkbox)
if checkbox:
    df_borne2
    

st.write("")
st.write("En bleu : bornes accessibles en extérieur")
st.write("En vert : bornes accessibles en intérieur")
     
# Visualisation de la carte avec Folium
## Si zone_emission = extérieur, on affiche une borne bleue.
# Dans les autres cas, on affiche une borne verte.    
    
m = folium.Map(location = [43.6042972191, 1.44397221945], zoom_start = 12)

for index, row in df_borne2.iterrows():
  if row.zone_emission == "extérieur":
    folium.Marker(location = row.coordonnee, popup = row.site, icon=folium.Icon(icon='wifi', prefix="fa", color='blue')).add_to(m)
  else:
    folium.Marker(location = row.coordonnee, popup = row.site, icon=folium.Icon(icon='wifi', prefix="fa", color='green')).add_to(m)

# call to render Folium map in Streamlit
folium_static(m)
