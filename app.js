const express = require('express');
const app = express();
const port = 5000;
const api = require('./api')

var swaggerUi = require('swagger-ui-express'),
    swaggerDocument = require('./swagger.json');

var options = {
  swaggerOptions: {
    tryItOutEnabled: true
  }
};

app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument, options));

app.use(express.json());
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.get('/votos/', api.getVotos);
app.get('/cargos/:id?', api.getCargos);
app.get('/cargosParaDistrito/:id?', api.getCargosForDistrict);
app.get('/agrupaciones/:nombre?', api.getAgrupaciones);
app.get('/mesas/:id?', api.getMesas);
app.get('/secciones/:id?', api.getSecciones);
app.get('/distritos/:id?', api.getDistritos);
app.get('/tiposVoto/:id?', api.getTiposVoto);
app.get('/porcentajes', api.getAgrupationPercentagesPerSection);
app.get('/votos/noPositivos', api.getNonPositive)
app.get('/votosConVariosParametros', api.getVotesMultipleParams)
app.get('/votos/noPositivos', api.getNonPositive);
app.get('/votosParaCargo', api.getVotesForPosition);
app.get('/fechas/', api.getDate);
app.get('/tipos/', api.getType);
app.get('/mesasYElectores/', api.getElectorsAndVotes);


// -------------------------------------------------------------------------


app.listen(port, () => {
  console.log('Elections app is running on port ' + port);
});
