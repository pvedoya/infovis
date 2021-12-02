import requests
import json
import pandas as pd
import altair as alt

r = requests.get('http://localhost:5000/votos-provincia?cargo=DIPUTADOS NACIONALES')
response = json.loads(r.text)

## climate ##

warm_states = ["Formosa", "Chaco", "Santiago del Estero", "Salta", "Misiones", "Corrientes", "Entre Ríos", "Tucumán"]

df = pd.DataFrame.from_records(response)
df['votos'] = pd.to_numeric(df['votos'])
# hot = df[df['distrito'].isin(warm_states)].groupby(by=["distrito", "agrupacion"])['votos'].agg('sum').to_frame().reset_index()
# hot = hot[hot['votos'] >= 20000]

# alt.Chart(hot, title="Resultados en provincias calurosas").mark_bar().encode(
#   x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
#   y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
#   color='distrito',
# ).show()

# cold_states = ["Chubut", "Río Negro", "Santa Cruz", "Neuquén", "Tierra del Fuego, Antártida e Islas del Atlántico Sur", "Mendoza", "San Luis", "La Pampa"]

# cold = df[df['distrito'].isin(cold_states)].groupby(by=["distrito", "agrupacion"])['votos'].agg('sum').to_frame().reset_index()
# cold = cold[cold['votos'] >= 10000]

# alt.Chart(cold, title="Resultados en provincias frías").mark_bar().encode(
#   x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
#   y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
#   color='distrito',
# ).show()

## population density ##

# populated = ["Ciudad Autónoma de Buenos Aires", "Buenos Aires", "Córdoba", "Santa Fe", "Mendoza", "Entre Ríos", "Salta", "Tucumán"]

# pop = df[df['distrito'].isin(populated)].groupby(by=["distrito", "agrupacion"])['votos'].agg('sum').to_frame().reset_index()
# pop = pop[pop['votos'] >= 50000]

# alt.Chart(pop, title="Resultados en provincias muy pobladas").mark_bar().encode(
#   x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
#   y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
#   color='distrito',
# ).show()

# less_populated = ["Tierra del Fuego, Antártida e Islas del Atlántico Sur", "Santa Cruz", "La Pampa", "La Rioja", "Catamarca", "San Luis", "Formosa", "Chubut"]

# less_pop = df[df['distrito'].isin(less_populated)].groupby(by=["distrito", "agrupacion"])['votos'].agg('sum').to_frame().reset_index()
# less_pop = less_pop[less_pop['votos'] >= 10000]

# alt.Chart(less_pop, title="Resultados en provincias poco pobladas").mark_bar().encode(
#   x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
#   y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
#   color='distrito',
# ).show()

## employment ##
# state_provinces = ["Formosa", "Jujuy", "Santiago del Estero", "La Rioja", "Catamarca", "Chaco", "Corrientes", "Salta"]

# state = df[df['distrito'].isin(state_provinces)].groupby(by=["distrito", "agrupacion"])['votos'].agg('sum').to_frame().reset_index()
# state = state[state['votos'] >= 20000]

# alt.Chart(state, title="Resultados en provincias con mayor empleo estatal").mark_bar().encode(
#   x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
#   y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
#   color='distrito',
# ).show()

# private_provinces = ["Ciudad Autónoma de Buenos Aires", "Córdoba", "Santa Fe", "Buenos Aires", "Chubut", "Mendoza", "Tierra del Fuego, Antártida e Islas del Atlántico Sur", "Río Negro"]

# private = df[df['distrito'].isin(private_provinces)].groupby(by=["distrito", "agrupacion"])['votos'].agg('sum').to_frame().reset_index()
# private = private[private['votos'] >= 10000]

# alt.Chart(private, title="Resultados en provincias con menor empleo estatal").mark_bar().encode(
#   x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
#   y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
#   color='distrito',
# ).show()

## terrain ##
# mountainous = ["Salta", "Jujuy", "Catamarca", "San Juan", "Chubut", "La Rioja", "Mendoza", "Tucumán"]

# elevated = df[df['distrito'].isin(mountainous)].groupby(by=["distrito", "agrupacion"])['votos'].agg('sum').to_frame().reset_index()
# elevated = elevated[elevated['votos'] >= 30000]

# alt.Chart(elevated, title="Resultados en provincias elevadas").mark_bar().encode(
#   x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
#   y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
#   color='distrito',
# ).show()

plains = ["Buenos Aires", "Ciudad Autónoma de Buenos Aires", "Misiones", "Corrientes", "Entre Ríos", "Santa Fe", "Chaco", "Río Negro"]

lowlands = df[df['distrito'].isin(plains)].groupby(by=["distrito", "agrupacion"])['votos'].agg('sum').to_frame().reset_index()
lowlands = lowlands[lowlands['votos'] >= 30000]

alt.Chart(lowlands, title="Resultados en provincias llanas").mark_bar().encode(
  x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
  y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
  color='distrito',
).show()