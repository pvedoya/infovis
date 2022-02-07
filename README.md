# infovis Q2-2021
## Proyecto Final - Elecciones Legislativas 2021
## Grupo 6: Florencia Monti, Juan Ignacio Quintairos y Pedro Vedoya  
  

### Carga de base de datos
Es necesario tener PostgreSQL instalado
- Descargar el archivo con el dump de la base [fixed_db.sql.zip](fixed_db.sql.zip)
- Extraer el archivo .sql
- Por línea de comandos ingresar: psql databasename < data_base_dump

Ahora se tiene la base de datos localmente.  
  

### Preparación del proyecto
Es necesario tener node.js instalado
- Descargar los archivos del proyecto y colocarlos en una carpeta
- Por línea de comandos, pararse en la carpeta anterior
- Correr: npm install

Esto instalará las librerías necesarias.  
  

### Correr el proyecto
- En la carpeta del proyecto correr: node app.js

Se debe ver un mensaje por la consola que indica el puerto en el que está corriendo el servicio.  
  

El mismo es el puerto 5000 y se tiene documentación de la API en:  

[Documentación API](http://localhost:5000/docs/)  
  
  
Los workbooks de ObservableHQ con las visualizaciones son los siguientes:  
  
[Análisis por partido, tipo y momento de carga. CABA](https://observablehq.com/@9f102930f24b5b7d/final-infovis/3)  

[Análisis por comunas. CABA](https://observablehq.com/@a3152d54413ef2ed/visualizacion-elecciones-legislativas-2021/2)  
