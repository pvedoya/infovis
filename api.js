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
  if(cargo == null) {
    cargo = "%";
  }
  const queryString = "SELECT Agrupacion, Distrito, votos "+
                      "FROM elecciones " +
                      "WHERE Cargo LIKE $1 ";

  pool.query(queryString, [cargo], (error, results) => {
    response.status(200).json(results.rows);
  });
};

const getCabaResults = async (request, response) => {
  let cargo = request.query.cargo;
  if(cargo == null) {
    cargo = "%";
  }
  const queryString = "SELECT Agrupacion, votos "+
                      "FROM elecciones " +
                      "WHERE Distrito LIKE 'Ciudad Aut%noma de Buenos Aires' AND Cargo LIKE $1 ";

  pool.query(queryString, [cargo], (error, results) => {
    response.status(200).json(results.rows);
  });
};

const getCabaSectionResults = async (request, response) => {
  let cargo = request.query.cargo;
  if(cargo == null) {
    cargo = "%";
  }
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

const getTableElectorsAndVotes = async (request, response) => {
  let distrito = request.query.distrito;
  if(distrito == null) {
    distrito = "%";
  }
  const queryString = "SELECT Distrito, Seccion, Mesa, electores, votos "+
                      "FROM elecciones " +
                      "WHERE Distrito LIKE $1 AND Cargo LIKE 'DIPUTADOS NACIONALES'";

  pool.query(queryString, [distrito], (error, results) => {
    response.status(200).json(results.rows);
  });
};

const getCabaPositions = async (request, response) => {
  const queryString = "SELECT DISTINCT Cargo " +
                      "FROM elecciones " +
                      "WHERE distrito LIKE 'Ciudad Aut%noma de Buenos Aires'";

  pool.query(queryString, (error, results) => {
    let cargos = [];
    results.rows.forEach(element => {
      cargos.push(element.cargo);
    });
    response.status(200).json(cargos);
  });
};

const getCabaAgrupationResults = async (request, response) => {
  let cargo = request.query.cargo;
  const queryString = "SELECT Agrupacion, SUM(votos) as votos, 100*SUM(votos)/(total::float) as porcentajeTotal " +
                      "FROM elecciones, ( " +
                        "SELECT SUM(votos) as total " +
                        "FROM elecciones " +
                        "WHERE Distrito LIKE 'Ciudad Aut%noma de Buenos Aires' AND Cargo LIKE $1 AND Agrupacion IS NOT NULL " +
                        ") as aux " +
                      "WHERE Distrito LIKE 'Ciudad Aut%noma de Buenos Aires' AND Cargo LIKE $1 AND Agrupacion IS NOT NULL " +
                      "GROUP BY Agrupacion, total";

  pool.query(queryString, [cargo], async(error, results) => {
    if (results != undefined){
      let answer = [];
      results.rows.forEach(element => {
        answer.push({agrupacion: element.agrupacion, votos: parseInt(element.votos), porcentajeTotal: parseFloat(element.porcentajetotal).toFixed(2)});
      });
      response.status(200).json(answer);
    }
    else
      response.status(200).json([]);
  });
};

const getTotalVotesForAgrupations = async (request, response) => {
  let cargo = request.query.cargo;
  const queryString = "SELECT SUM(votos) as total " +
                      "FROM elecciones " +
                      "WHERE Distrito LIKE 'Ciudad Aut%noma de Buenos Aires' AND Cargo LIKE $1 AND Agrupacion IS NOT NULL ";

  pool.query(queryString, [cargo], (error, results) => {
    if (results != undefined){
      response.status(200).json(parseInt(results.rows[0].total));
    }
    else
      response.status(500).json();
  });
};

const getCabaAgrupationPercentagesPerSection = async (request, response) => {
  let cargo = request.query.cargo;
  const queryString = "SELECT Agrupacion, seccion, 100 * SUM(votos) / totalComuna::float as porcentaje " +
                      "FROM elecciones NATURAL JOIN ( " +
                        "SELECT seccion, SUM(votos) as totalComuna " +
                        "FROM elecciones " +
                        "WHERE Distrito LIKE 'Ciudad Aut%noma de Buenos Aires' AND Cargo LIKE $1 AND Agrupacion IS NOT NULL " +
                        "GROUP BY seccion " +
                        ") as aux " +
                      "WHERE Distrito LIKE 'Ciudad Aut%noma de Buenos Aires' AND Cargo LIKE $1 AND Agrupacion IS NOT NULL " +
                      "GROUP BY Agrupacion, seccion, totalComuna;";

  pool.query(queryString, [cargo], async(error, results) => {
    if (results != undefined){
      let answer = [];
      results.rows.forEach(element => {
        answer.push({agrupacion: element.agrupacion, comuna: (element.seccion), porcentaje: parseFloat(element.porcentaje).toFixed(2)});
      });
      response.status(200).json(answer);
    }
    else
      response.status(200).json([]);
  });
};

const getCabaResultsByAgr = async (request, response) => {
  let cargo = request.query.cargo;
  const queryString = "SELECT agrupacion, SUM(CAST(votos AS INTEGER)) AS votos " +
                      "FROM public.elecciones " +
                      "WHERE distrito LIKE 'Ciudad Aut%noma de Buenos Aires' AND cargo LIKE $1 AND agrupacion IS NOT NULL " +
                      "GROUP BY agrupacion " +
                      "ORDER BY votos ";

  pool.query(queryString, [cargo], (error, results) => {
    response.status(200).json(results.rows);
  });
};

const getTipoVotos = async (request, response) => {
  let cargo = request.query.cargo;
  const queryString = "SELECT tipovotos, SUM(CAST(votos AS INTEGER)) AS votos " +
                      "FROM public.elecciones " +
                      "WHERE distrito LIKE 'Ciudad Aut%noma de Buenos Aires' AND cargo LIKE $1 " +
                      "GROUP BY tipovotos " +
                      "ORDER BY votos ";

  pool.query(queryString, [cargo], (error, results) => {
    response.status(200).json(results.rows);
  });
};

const getVotosPosNeg = async (request, response) => {
  let cargo = request.query.cargo;
  const queryString = "SELECT 'no positivo' as tipovotos, SUM(CAST(votos AS INTEGER)) AS votos " +
                      "FROM public.elecciones " +
                      "WHERE distrito LIKE 'Ciudad Aut%noma de Buenos Aires' AND cargo LIKE $1 AND tipovotos IN ('nulos', 'recurridos', 'blancos', 'impugnados') " +
                      "UNION SELECT tipovotos, SUM(CAST(votos AS INTEGER)) AS votos " +
                      "FROM public.elecciones " +
                      "WHERE distrito LIKE 'Ciudad Aut%noma de Buenos Aires' AND cargo LIKE $1 AND tipovotos IN ('positivo') " +
                      "GROUP BY tipovotos ";

  pool.query(queryString, [cargo], (error, results) => {
    response.status(200).json(results.rows);
  });
};

const getFecha = async (request, response) => {
  let cargo = request.query.cargo;
  const queryString = "SELECT agrupacion, SUM(CAST(votos as INTEGER)) as votos, fecha " +
                      "FROM public.elecciones " +
                      "WHERE distrito LIKE 'Ciudad Aut%noma de Buenos Aires' AND cargo LIKE $1 AND agrupacion IS NOT NULL " +
                      "GROUP BY fecha, agrupacion ";

  pool.query(queryString, [cargo], (error, results) => {
    if (results != undefined){
      let answer = [];
      results.rows.forEach(element => {
        answer.push({agrupacion: element.agrupacion, votos: parseInt(element.votos), fecha: element.fecha});
      });
      response.status(200).json(answer);
    }
    else
      response.status(200).json([]);
  });
};

module.exports = {
  getEntries,
  getCabaResults,
  getCabaSectionResults,
  getNonPositive,
  getTableElectorsAndVotes,
  getCabaPositions,
  getCabaAgrupationResults,
  getTotalVotesForAgrupations,
  getCabaAgrupationPercentagesPerSection,
  getCabaResultsByAgr,
  getTipoVotos,
  getVotosPosNeg,
  getFecha
}
