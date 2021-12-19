import requests
import json
import pandas as pd
import altair as alt

partidos = ["AUTODETERMINACIÓN Y LIBERTAD", "FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD", "FRENTE DE TODOS", "JUNTOS POR EL CAMBIO", "LA LIBERTAD AVANZA"]

############################################################## part A ##############################################################

r = requests.get('http://localhost:5000/caba-results?cargo=DIPUTADOS NACIONALES')
response = json.loads(r.text)

df = pd.DataFrame.from_records(response)
df['votos'] = pd.to_numeric(df['votos'])
df = df.groupby(by=["agrupacion"])['votos'].agg('sum').to_frame().reset_index()

total = df['votos'].agg('sum')
percentage = []

for idx, row in df.iterrows():
  percentage.append(row['votos']/total)

total_df = pd.DataFrame({
  'agrupacion': df['agrupacion'],
  'porcentaje': percentage
})

alt.Chart(total_df, title="Porcentaje de votos por partido en CABA(Diputados Nacionales)").mark_bar().encode(
  y=alt.Y('agrupacion:N', sort='x', axis=alt.Axis(title='Agrupación')),
  x=alt.X('porcentaje:Q', axis=alt.Axis(format='.0%', title='Porcentaje')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain=partidos, range=["blue", "red", "cyan", "yellow","green" ]), title="Agrupación")
).show()

############################################################## part B ##############################################################

r = requests.get('http://localhost:5000/caba-results?cargo=DIPUTADOS PROVINCIALES')
response = json.loads(r.text)

df = pd.DataFrame.from_records(response)
df['votos'] = pd.to_numeric(df['votos'])
df = df.groupby(by=["agrupacion"])['votos'].agg('sum').to_frame().reset_index()

total = df['votos'].agg('sum')
percentage = []

for idx, row in df.iterrows():
  percentage.append(row['votos']/total)

total_df = pd.DataFrame({
  'agrupacion': df['agrupacion'],
  'porcentaje': percentage
})

alt.Chart(total_df,title="Porcentaje de votos por partido en CABA (Diputados Provinciales)").mark_bar().encode(
  y=alt.Y('agrupacion:N', sort='x', axis=alt.Axis(title='Agrupación')),
  x=alt.X('porcentaje:Q', axis=alt.Axis(format='.0%', title='Porcentaje')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain=partidos, range=["blue", "red", "cyan", "yellow","green" ]), title="Agrupación")
).show()

############################################################## part C ##############################################################

r = requests.get('http://localhost:5000/caba-section-results?cargo=DIPUTADOS NACIONALES')
response = json.loads(r.text)

df = pd.DataFrame.from_records(response)
df['votos'] = pd.to_numeric(df['votos'])
df = df.groupby(by=["seccion", "agrupacion"])['votos'].agg('sum').to_frame().reset_index()

total = df['votos'].agg('sum')
percentage = []

for idx, row in df.iterrows():
  percentage.append(row['votos']/total)

total_df = pd.DataFrame({
  'agrupacion': df['agrupacion'],
  'seccion': df['seccion'],
  'porcentaje': percentage
})

alt.Chart(total_df,title="Porcentaje de votos por comuna de CABA (Diputados Nacionales)").mark_bar().encode(
  x=alt.X('sum(porcentaje)', axis=alt.Axis(format='.0%', title='Porcentaje')),
  y=alt.Y('seccion', sort='-x', axis=alt.Axis(title='Sección')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain=partidos, range=["blue", "red", "cyan", "yellow","green" ]), title="Agrupación")
).show()

############################################################## part D ##############################################################

r = requests.get('http://localhost:5000/caba-section-results?cargo=DIPUTADOS PROVINCIALES')
response = json.loads(r.text)

df = pd.DataFrame.from_records(response)
df['votos'] = pd.to_numeric(df['votos'])
df = df.groupby(by=["seccion", "agrupacion"])['votos'].agg('sum').to_frame().reset_index()

total = df['votos'].agg('sum')
percentage = []

for idx, row in df.iterrows():
  percentage.append(row['votos']/total)

total_df = pd.DataFrame({
  'agrupacion': df['agrupacion'],
  'seccion': df['seccion'],
  'porcentaje': percentage
})

alt.Chart(total_df,title="Porcentaje de votos por comuna de CABA (Diputados Provinciales)").mark_bar().encode(
  x=alt.X('sum(porcentaje)', axis=alt.Axis(format='.0%', title='Porcentaje')),
  y=alt.Y('seccion', sort='-x', axis=alt.Axis(title='Sección')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain=partidos, range=["blue", "red", "cyan", "yellow","green" ]), title="Agrupación")
).show()
