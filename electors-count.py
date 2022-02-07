import requests
import json
import pandas as pd
import altair as alt

############################################################## part A ##############################################################

r = requests.get('http://localhost:5000/mesasYElectores?distrito=Ciudad Autónoma de Buenos Aires')
print("Got response")
response = json.loads(r.text)

df = pd.DataFrame.from_records(response)
df['votos'] = pd.to_numeric(df['votos'])
df['electores'] = pd.to_numeric(df['electores'])

electors = df.groupby(by=["seccion"])['electores'].mean().to_frame().reset_index()

df = df.groupby(by=["seccion", "mesa"])['votos'].agg('sum').to_frame().reset_index()
df = df.groupby(by=["seccion"])['votos'].mean().to_frame().reset_index()

bar = alt.Chart(df).mark_bar().encode(
  x=alt.X('seccion:O', axis=alt.Axis(title='Sección')),
  y=alt.Y('votos:Q', sort='-x', axis=alt.Axis(title='Promedio de votos por mesa'))
)

mean_electors_present = alt.Chart(df).mark_rule(color='red').encode(
    y='mean(votos):Q'
)

electors_line = alt.Chart(electors).mark_rule(color='blue').encode(
    y='mean(electores):Q'
)

(bar + mean_electors_present + electors_line).show()