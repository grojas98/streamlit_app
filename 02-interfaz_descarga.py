# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 11:48:09 2022

@author: groja
"""

import streamlit as st
import pandas as pd
import psycopg2 as pg
import base64
import datetime
from PIL import Image

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="file.csv">Descargar archivo CSV</a>'
    return href
#%%
ht_2 = Image.open('ht2.jfif')
ht = Image.open('logo.png')

#%%
db_pctes = "database_pctes.xlsx"
db_pctes_df = pd.read_excel(db_pctes)
pct_tup = list(db_pctes_df['Paciente'])
pct_tup = tuple(pct_tup)

#%%
#connect to db
con = pg.connect(
    host = '192.168.1.163',
    user = 'postgres',
    password = 'somno2019',
    port = '9001',
    database = 'somno')

#cursor
cur = con.cursor()

#%%

col1, mid, col2 = st.columns([1,5,1])
with col1:
    st.image('logo.png', width=90)
with mid:
    st.markdown("<h1 style='text-align: center; color: black;'>Interfaz de descarga archivo CSV</h1>", unsafe_allow_html=True)

st.write('Interfaz destinada a la descarga del archivo CSV con información de sensores, desarrollado por ***Healthtracker***')

option = st.selectbox(
      'Seleccionar paciente',
      pct_tup)


index_db = db_pctes_df.index[db_pctes_df['Paciente'] == option]
db_option = db_pctes_df.loc[db_pctes_df['Paciente'] == option]
db_rut = db_pctes_df['Rut'].loc[db_pctes_df['Paciente'] == option]
db_sabana = db_pctes_df['Sabana'].loc[db_pctes_df['Paciente'] == option]
db_mac = db_option['MAC'][index_db[0]]

# st.write('Paciente seleccionado:', option)

#%% SIDEBAR
st.sidebar.image(ht_2, width=200)
st.sidebar.header('Información de paciente')
st.sidebar.write('Nombre paciente:', str(option))
st.sidebar.write('Rut paciente:', str(db_rut[index_db[0]]))
st.sidebar.write('N° Sabana en uso:', str(db_sabana[index_db[0]]))
st.sidebar.write('MAC address:', str(db_mac).replace('mac_',''))

#%%
time_stamp_2 = ('1 hour','5 hours','12 hours','1 day','2 days')
time_stamp = ('1 hora','5 horas','12 horas','1 día','2 días')
#%%

st.header("""
    Descargar archivo CSV de datos de sábana de acuerdo a rango de fechas: 
         """)

d1 = datetime.date.today()
d2 = d1 + datetime.timedelta(days=1)
st.write("""
    **Seleccionar fecha:**
         """)

start_date = st.date_input('Desde:', d1)
t1 = st.time_input('Hora:', datetime.time(00, 00),key=0)
end_date = st.date_input('Hasta:', d2)
t2 = st.time_input('Hora:', datetime.time(00, 15),key=1)

if start_date <= end_date and t1 < t2:
    start_date = str(start_date) + ' ' + str(t1)
    end_date = str(end_date) + ' ' + str(t2)
    st.success('Desde: `%s`\n\nHasta: `%s`' % (start_date[:-3], end_date[:-3]))
    postgreSQL_select_Query_2 = "select * from " + str(db_mac) + " where time between " + "'" + start_date + "'" + " and " + "'" + end_date + "'"
    # print(postgreSQL_select_Query_2)
    cur.execute(postgreSQL_select_Query_2)
    mobile_records_2 = cur.fetchall()
    log_df = pd.DataFrame(mobile_records_2)
    st.markdown(filedownload(log_df), unsafe_allow_html=True)
else:
    st.error('Error: Rango de fechas inválido.')
    pass

st.header("""
    Descargar archivo CSV de datos de sábana en las últimas: 
         """)

select_time = st.radio(
     'Seleccionar tiempo a descargar:',
     time_stamp)
time_stamp = list(time_stamp)
time_stamp_2 = list(time_stamp_2)

for i in range(len(time_stamp)):
    if str(select_time) == time_stamp[i]:
        select_time = time_stamp_2[i]

postgreSQL_select_Query_2 = "select * from " + str(db_mac) + " where time >= NOW() - " + "'" + str(select_time) + "'" + "::INTERVAL"

cur.execute(postgreSQL_select_Query_2)
mobile_records_2 = cur.fetchall()

log_df = pd.DataFrame(mobile_records_2)

st.markdown(filedownload(log_df), unsafe_allow_html=True)

#close cursor
cur.close()

#close connection
con.close()




