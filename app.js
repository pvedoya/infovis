const express = require('express');
const app = express();
const port = 5000;
const api = require('./api')

app.use(express.json());
app.get('/votos-provincia/', api.getEntries);
app.get('/caba-results/', api.getCabaResults);
app.get('/caba-section-results/', api.getCabaSectionResults);
app.get('/non-positive-results/', api.getNonPositive);

app.listen(port, () => {
  console.log('Elections app is running on port ' + port);
});