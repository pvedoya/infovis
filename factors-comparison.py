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
hot = df[df['distrito'].isin(warm_states)].groupby(by=["agrupacion"])['votos'].agg('sum').to_frame().reset_index()
hot = hot[hot['votos'] >= 100000]

alt.Chart(hot, title="Resultados en provincias calurosas").mark_bar().encode(
  x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
  y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain=["JUNTOS POR EL CAMBIO", "FRENTE DE TODOS", "FRENTE RENOVADOR DE LA CONCORDIA", "FUERZA REPUBLICANA"], range=["yellow", "cyan", "orange", "blue"]))
).show()

cold_states = ["Chubut", "Río Negro", "Santa Cruz", "Neuquén", "Tierra del Fuego, Antártida e Islas del Atlántico Sur", "Mendoza", "San Luis", "La Pampa"]

cold = df[df['distrito'].isin(cold_states)].groupby(by=["agrupacion"])['votos'].agg('sum').to_frame().reset_index()
cold = cold[cold['votos'] >= 100000]

alt.Chart(cold, title="Resultados en provincias frías").mark_bar().encode(
  x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
  y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain=["JUNTOS POR EL CAMBIO", "FRENTE DE TODOS", "FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD", "MOVIMIENTO POPULAR NEUQUINO"], range=["yellow", "cyan", "red", "green"]))
).show()

## population density ##

populated = ["Ciudad Autónoma de Buenos Aires", "Buenos Aires", "Córdoba", "Santa Fe", "Mendoza", "Entre Ríos", "Salta", "Tucumán"]

pop = df[df['distrito'].isin(populated)].groupby(by=["agrupacion"])['votos'].agg('sum').to_frame().reset_index()
pop = pop[pop['votos'] >= 150000]

alt.Chart(pop, title="Resultados en provincias muy pobladas").mark_bar().encode(
  x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
  y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain = ["JUNTOS POR EL CAMBIO", "FRENTE DE TODOS", "FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD", "HACEMOS POR CÓRDOBA", "AVANZA LIBERTAD", "FRENTE VAMOS CON VOS", "LA LIBERTAD AVANZA", "FRENTE AMPLIO PROGRESISTA", "+ VALORES"], range=["yellow", "cyan", "red", "orange", "blue", "pink", "green", "purple", "grey"]))
).show()

less_populated = ["Tierra del Fuego, Antártida e Islas del Atlántico Sur", "Santa Cruz", "La Pampa", "La Rioja", "Catamarca", "San Luis", "Formosa", "Chubut"]

less_pop = df[df['distrito'].isin(less_populated)].groupby(by=["agrupacion"])['votos'].agg('sum').to_frame().reset_index()
less_pop = less_pop[less_pop['votos'] >= 100000]

alt.Chart(less_pop, title="Resultados en provincias poco pobladas").mark_bar().encode(
  x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
  y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain=["JUNTOS POR EL CAMBIO", "FRENTE DE TODOS"], range=["yellow", "cyan"]))
).show()

## employment ##
state_provinces = ["Formosa", "Jujuy", "Santiago del Estero", "La Rioja", "Catamarca", "Chaco", "Corrientes", "Salta"]

state = df[df['distrito'].isin(state_provinces)].groupby(by=["agrupacion"])['votos'].agg('sum').to_frame().reset_index()
state = state[state['votos'] >= 100000]

alt.Chart(state, title="Resultados en provincias con mayor empleo estatal").mark_bar().encode(
  x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
  y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain=["JUNTOS POR EL CAMBIO", "FRENTE DE TODOS","FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD"], range=["yellow", "cyan", "red"]))
).show()

private_provinces = ["Ciudad Autónoma de Buenos Aires", "Córdoba", "Santa Fe", "Buenos Aires", "Chubut", "Mendoza", "Tierra del Fuego, Antártida e Islas del Atlántico Sur", "Río Negro"]

private = df[df['distrito'].isin(private_provinces)].groupby(by=["agrupacion"])['votos'].agg('sum').to_frame().reset_index()
private = private[private['votos'] >= 100000]

alt.Chart(private, title="Resultados en provincias con menor empleo estatal").mark_bar().encode(
  x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
  y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain = ["JUNTOS POR EL CAMBIO", "FRENTE DE TODOS", "FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD", "HACEMOS POR CÓRDOBA", "AVANZA LIBERTAD", "FRENTE VAMOS CON VOS", "LA LIBERTAD AVANZA", "FRENTE AMPLIO PROGRESISTA", "+ VALORES"], range=["yellow", "cyan", "red", "orange", "blue", "pink", "green", "purple", "grey"]))
).show()

## terrain ##
mountainous = ["Salta", "Jujuy", "Catamarca", "San Juan", "Chubut", "La Rioja", "Mendoza", "Tucumán"]

elevated = df[df['distrito'].isin(mountainous)].groupby(by=["agrupacion"])['votos'].agg('sum').to_frame().reset_index()
elevated = elevated[elevated['votos'] >= 100000]

alt.Chart(elevated, title="Resultados en provincias elevadas").mark_bar().encode(
  x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
  y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain=["JUNTOS POR EL CAMBIO", "FRENTE DE TODOS","FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD", "FUERZA REPUBLICANA"], range=["yellow", "cyan", "red", "blue"]))
).show()

plains = ["Buenos Aires", "Ciudad Autónoma de Buenos Aires", "Misiones", "Corrientes", "Entre Ríos", "Santa Fe", "Chaco", "Río Negro"]

lowlands = df[df['distrito'].isin(plains)].groupby(by=["agrupacion"])['votos'].agg('sum').to_frame().reset_index()
lowlands = lowlands[lowlands['votos'] >= 100000]

alt.Chart(lowlands, title="Resultados en provincias llanas").mark_bar().encode(
  x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
  y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain = ["JUNTOS POR EL CAMBIO", "FRENTE DE TODOS", "FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD", "FRENTE RENOVADOR DE LA CONCORDIA", "AVANZA LIBERTAD", "FRENTE VAMOS CON VOS", "LA LIBERTAD AVANZA", "FRENTE AMPLIO PROGRESISTA", "+ VALORES"], range=["yellow", "cyan", "red", "orange", "blue", "pink", "green", "purple", "grey"]))
).show()

## hdi ##
high = ["Tierra del Fuego, Antártida e Islas del Atlántico Sur", "Ciudad Autónoma de Buenos Aires", "Chubut", "Santa Cruz", "La Pampa", "Neuquén", "San Luis", "Córdoba"]

high_hdi = df[df['distrito'].isin(high)].groupby(by=["agrupacion"])['votos'].agg('sum').to_frame().reset_index()
high_hdi = high_hdi[high_hdi['votos'] >= 100000]

alt.Chart(high_hdi, title="Resultados en provincias con alto IDH").mark_bar().encode(
  x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
  y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain = ["JUNTOS POR EL CAMBIO", "FRENTE DE TODOS", "FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD", "HACEMOS POR CÓRDOBA", "LA LIBERTAD AVANZA", "MOVIMIENTO POPULAR NEUQUINO"], range=["yellow", "cyan", "red", "orange", "green", "blue"]))
).show()

low = ["Chaco", "Santiago del Estero", "Formosa", "Corrientes", "Misiones", "Salta", "La Rioja", "Jujuy"]

low_hdi = df[df['distrito'].isin(low)].groupby(by=["agrupacion"])['votos'].agg('sum').to_frame().reset_index()
low_hdi = low_hdi[low_hdi['votos'] >= 100000]

alt.Chart(low_hdi, title="Resultados en provincias con bajo IDH").mark_bar().encode(
  x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
  y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain = ["JUNTOS POR EL CAMBIO", "FRENTE DE TODOS", "FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD", "FRENTE RENOVADOR DE LA CONCORDIA"], range=["yellow", "cyan", "red", "orange"]))
).show()

## size ##
big = ["Buenos Aires", "Santa Cruz", "Chubut", "Río Negro", "Córdoba", "Salta", "Mendoza", "La Pampa"]

big_provinces = df[df['distrito'].isin(big)].groupby(by=["agrupacion"])['votos'].agg('sum').to_frame().reset_index()
big_provinces = big_provinces[big_provinces['votos'] >= 100000]

alt.Chart(big_provinces, title="Resultados en provincias con bajo IDH").mark_bar().encode(
  x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
  y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain = ["JUNTOS POR EL CAMBIO", "FRENTE DE TODOS", "FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD", "HACEMOS POR CÓRDOBA", "AVANZA LIBERTAD", "FRENTE VAMOS CON VOS", "+ VALORES"], range=["yellow", "cyan", "red", "orange", "blue", "pink", "grey"]))
).show()

small = ["Ciudad Autónoma de Buenos Aires", "Tierra del Fuego, Antártida e Islas del Atlántico Sur", "Tucumán", "Misiones", "Jujuy", "Formosa", "San Luis", "Entre Ríos"]

small_provinces = df[df['distrito'].isin(small)].groupby(by=["agrupacion"])['votos'].agg('sum').to_frame().reset_index()
small_provinces = small_provinces[small_provinces['votos'] >= 100000]

alt.Chart(small_provinces, title="Resultados en provincias con bajo IDH").mark_bar().encode(
  x=alt.X('sum(votos)', axis=alt.Axis(title='Votos')),
  y=alt.Y('agrupacion', sort='-x', axis=alt.Axis(title='Agrupación')),
  color=alt.Color('agrupacion:N', scale=alt.Scale(domain = ["JUNTOS POR EL CAMBIO", "FRENTE DE TODOS", "FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD", "LA LIBERTAD AVANZA", "FRENTE RENOVADOR DE LA CONCORDIA", "FUERZA REPUBLICANA"], range=["yellow", "cyan", "red", "green", "orange", "blue"]))
).show()