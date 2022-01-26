import requests
import json
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

electors = {
    "Buenos Aires": 12704518,
    "Catamarca": 327478,
    "Chaco": 967147,
    "Chubut": 448149,
    "Ciudad Autónoma de Buenos Aires": 2552058,
    "Córdoba": 2984631,
    "Corrientes": 894376,
    "Entre Ríos": 1112939,
    "Formosa": 468299,
    "Jujuy": 573326,
    "La Pampa": 293790,
    "La Rioja" : 294509,
    "Mendoza": 1439463,
    "Misiones": 948500,
    "Neuquén": 526441,
    "Río Negro": 560880,
    "Salta": 1051142,
    "San Juan": 579913,
    "San Luis": 393472,
    "Santa Cruz": 256388,
    "Santa Fe": 2768525,
    "Santiago del Estero": 778455,
    "Tierra del Fuego, Antártida e Islas del Atlántico Sur": 141548,
    "Tucumán": 1267045,
}

############################################################## part A ##############################################################

r = requests.get('http://localhost:5000/votos/noPositivos?distrito=Ciudad Aut%noma de Buenos Aires')
response = json.loads(r.text)

df = pd.DataFrame.from_records(response)
df['votos'] = pd.to_numeric(df['votos'])
df = df.groupby(by=["seccion", "tipo"])['votos'].agg('sum').to_frame().reset_index()

alt.Chart(df, title="Votos no positivos en CABA").mark_bar(
  cornerRadiusTopLeft = 3,
  cornerRadiusTopRight = 3
).encode(
  x=alt.X('sum(votos):Q', axis=alt.Axis(title='Votos')),
  y=alt.Y('seccion:O', sort='-x', axis=alt.Axis(title='Sección')),
  color=alt.Color('tipo:N', title="Tipo de Voto"),
  order=alt.Order(
    'tipo',
    sort='ascending'
  )
).show()

############################################################## part B ##############################################################

top_districts = ["La Matanza", "La Plata", "General Pueyrredón", "Lomas de Zamora", "Quilmes", "Almirante Brown", "Merlo", "Lanús", "Moreno", "Florencio Varela", "General San Martín", "Tigre", "Avellaneda", "Tres de Febrero", "Berazategui"]

r = requests.get('http://localhost:5000/votos/noPositivos?distrito=Buenos Aires')
response = json.loads(r.text)

df = pd.DataFrame.from_records(response)
df['votos'] = pd.to_numeric(df['votos'])
df = df[df['seccion'].isin(top_districts)].groupby(by=["seccion", "tipo"])['votos'].agg('sum').to_frame().reset_index()

alt.Chart(df, title="Votos no positivos en PBA").mark_bar(
  cornerRadiusTopLeft = 3,
  cornerRadiusTopRight = 3
).encode(
  x=alt.X('sum(votos):Q', axis=alt.Axis(title='Votos')),
  y=alt.Y('seccion:O', sort='-x', axis=alt.Axis(title='Sección')),
  color=alt.Color('tipo:N', title="Tipo de Voto"),
  order=alt.Order(
    'tipo',
    sort='ascending'
  )
).show()

############################################################## part C ##############################################################

r = requests.get('http://localhost:5000/votos/noPositivos')
response = json.loads(r.text)

df = pd.DataFrame.from_records(response)
df['votos'] = pd.to_numeric(df['votos'])
df = df.groupby(by=["distrito", "tipo"])['votos'].agg('sum').to_frame().reset_index()

alt.Chart(df, title="Votos no positivos en Argentina").mark_bar(
  cornerRadiusTopLeft = 3,
  cornerRadiusTopRight = 3
).encode(
  x=alt.X('sum(votos):Q', axis=alt.Axis(title='Votos')),
  y=alt.Y('distrito:O', sort='-x', axis=alt.Axis(title='Distrito')),
  color=alt.Color('tipo:N', title="Tipo de Voto"),
  order=alt.Order(
    'tipo',
    sort='ascending'
  )
).show()

############################################################## part D ##############################################################

r = requests.get('http://localhost:5000/votosParaCargo?cargo=DIPUTADOS NACIONALES')
response = json.loads(r.text)

df = pd.DataFrame.from_records(response)
df['votos'] = pd.to_numeric(df['votos'])
df = df.groupby(by=["distrito"])['votos'].agg('sum').to_frame().reset_index()

percentage = []

for idx, row in df.iterrows():
  value = int(100-(row['votos']/electors[row['distrito']])*100)
  percentage.append(value)

total_df = pd.DataFrame({
  'distrito': df['distrito'],
  'porcentaje': percentage
})

fig = go.Figure([go.Bar(x=total_df['porcentaje'], y=total_df['distrito'], orientation='h', text=total_df['porcentaje'], textposition='outside', hoverinfo='skip')])
fig.update_layout(xaxis_range=[0,40],
                  yaxis={'title': 'x-axis','fixedrange':True},
                  xaxis={'title': 'y-axis','fixedrange':True},
                  title="Porcentaje de abstención electoral por provincia (Diputados Nacionales)",
                  xaxis_title="Abstención del padrón (%)")

fig.show()

############################################################## part E ##############################################################

r = requests.get('http://localhost:5000/votosParaCargo?cargo=SENADORES NACIONALES')
response = json.loads(r.text)

df = pd.DataFrame.from_records(response)
df['votos'] = pd.to_numeric(df['votos'])
df = df.groupby(by=["distrito"])['votos'].agg('sum').to_frame().reset_index()

percentage = []

for idx, row in df.iterrows():
  value = int(100-(row['votos']/electors[row['distrito']])*100)
  percentage.append(value)

total_df = pd.DataFrame({
  'distrito': df['distrito'],
  'porcentaje': percentage
})

fig = go.Figure([go.Bar(x=total_df['porcentaje'], y=total_df['distrito'], orientation='h', text=total_df['porcentaje'], textposition='outside', hoverinfo='skip')])
fig.update_layout(xaxis_range=[0,40],
                  yaxis={'title': 'x-axis','fixedrange':True},
                  xaxis={'title': 'y-axis','fixedrange':True},
                  title="Porcentaje de abstención electoral por provincia (Senadores Nacionales)",
                  xaxis_title="Abstención del padrón (%)")

fig.show()
