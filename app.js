const express = require('express');
const app = express();
const port = 5000;
const api = require('./api')

app.use(express.json());
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "https://a3152d54413ef2ed.static.observableusercontent.com");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});
app.get('/votos-provincia/', api.getEntries);
app.get('/caba-results/', api.getCabaResults);
app.get('/caba-section-results/', api.getCabaSectionResults);
app.get('/non-positive-results/', api.getNonPositive);
app.get('/electors-and-votes/', api.getTableElectorsAndVotes);
app.get('/caba-positions/', api.getCabaPositions);
app.get('/caba-agrupation-results/', api.getCabaAgrupationResults);
app.get('/caba-votes-for-agrupations/', api.getTotalVotesForAgrupations);
app.get('/caba-agrupations-percentages-per-section/', api.getCabaAgrupationPercentagesPerSection);

app.listen(port, () => {
  console.log('Elections app is running on port ' + port);
});