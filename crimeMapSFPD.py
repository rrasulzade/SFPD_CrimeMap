import folium
from folium.plugins import MarkerCluster
import pandas as pd
import json


SF_COORDINATES = [37.76, -122.45]

crimedata = pd.read_csv('SFPD_incident_2017_.csv')

MAX_RECORDS = 1000


map = folium.Map(location=[37.76, -122.45], tiles='Stamen Toner', zoom_start=12)

marker_cluster = MarkerCluster(
    name='1000 clustered icons',
    overlay=True,
    control=False,
    icon_create_function=None
)


fg = folium.FeatureGroup(name="SFPD Incidents")
for each in crimedata.iterrows(): #[0:MAX_RECORDS].iterrows():
    marker = folium.Marker(location=[each[1]['Y'],each[1]['X']])
    marker_cluster.add_child(marker)


district_geo = r'sfpd_districts2.json'


crimedata2 = pd.DataFrame(crimedata['PdDistrict'].value_counts().astype(float))
crimedata2.to_json('crimeagg.json')
crimedata2 = crimedata2.reset_index()
crimedata2.columns = ['District', 'Number']


map.choropleth(
    geo_data=district_geo,
    name='choropleth',
    data=crimedata2,
    columns=['District', 'Number'],
    key_on='feature.properties.DISTRICT',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Number of incidents per district'
)


# map.add_child(fg)
# map.add_child(folium.LayerControl())
marker_cluster.add_to(map)
folium.LayerControl().add_to(map)
map.save("crimeMapSFPD.html")
