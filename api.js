const Pool = require('pg').Pool;

const pool = new Pool({
  user: 'petrvs',
  host: 'localhost',
  database: 'infovis',
  password: 'infovis-final',
  port: 5432
});

const getEntries = async (request, response) => {
  let cargo = request.query.cargo;
  const queryString = "SELECT Agrupacion, Distrito, votos "+
                      "FROM elecciones " +
                      "WHERE Cargo LIKE $1 ";

  pool.query(queryString, [cargo], (error, results) => {
    response.status(200).json(results.rows);
  });
};

const getCabaResults = async (request, response) => {
  let cargo = request.query.cargo;
  const queryString = "SELECT Agrupacion, votos "+
                      "FROM elecciones " +
                      "WHERE Distrito LIKE 'Ciudad Aut%noma de Buenos Aires' AND Cargo LIKE $1 ";

  pool.query(queryString, [cargo], (error, results) => {
    response.status(200).json(results.rows);
  });
};

const getCabaSectionResults = async (request, response) => {
  let cargo = request.query.cargo;
  const queryString = "SELECT Agrupacion, Seccion, votos "+
                      "FROM elecciones " +
                      "WHERE Distrito LIKE 'Ciudad Aut%noma de Buenos Aires' AND Cargo LIKE $1 ";

  pool.query(queryString, [cargo], (error, results) => {
    response.status(200).json(results.rows);
  });
};

const getNonPositive = async (request, response) => {
  let distrito = request.query.distrito;
  if(distrito == null) {
    distrito = "%";
  }
  const queryString = "SELECT Distrito, Seccion, tipoVotos, votos "+
                      "FROM elecciones " +
                      "WHERE Distrito LIKE $1 AND Cargo LIKE 'DIPUTADOS NACIONALES' AND tipoVotos IN ('nulos', 'recurridos', 'blancos', 'impugnados') ";

  pool.query(queryString, [distrito], (error, results) => {
    response.status(200).json(results.rows);
  });
};

module.exports = {
  getEntries,
  getCabaResults,
  getCabaSectionResults,
  getNonPositive
}