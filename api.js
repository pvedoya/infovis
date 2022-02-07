const Pool = require('pg').Pool;

const Joi = require('joi');

const pool = new Pool({
  user: 'petrvs',
  host: 'localhost',
  database: 'infovis',
  password: 'infovis-final',
  port: 5432
});


// -------------------------------------------------------------------------

const validateVotosParams = (params) => {
  let schema = { 
    groupBy: Joi.string(),
    mesa: Joi.number().min(0),
    seccion: Joi.number().min(0),
    distrito : Joi.number().min(0),
    cargo : Joi.number().min(0),
    agrupacion : Joi.number().min(0),
    fecha : Joi.string()
  };
         
  if (!Joi.validate(params,schema))
    return false;

  if(params.groupBy == undefined)   //Si no hay groupBy listo, sino lo tengo que revisar
    return true;

  const groupByValue = params.groupBy.toLowerCase();

  //Check if the parameter is one of the sortBy values

  let groupByParameters = ['idmesa', 'idseccion', 'iddistrito', 'agrupacion', 'idtipo', 'idcargo', 'fecha'];

  let i;
  let elem;
  let found = false;
  for(i = 0; !found && i < groupByParameters.length; i++){
      elem = groupByParameters[i].toLowerCase();
      if(groupByValue == elem.toLowerCase()){                    
          found = true;
      }
  }

  return found;
}

const parseWhere = (params) => {
  let whereParameters = ['idmesa', 'idseccion', 'iddistrito', 'agrupacion', 'idtipo', 'idcargo', 'fecha'];
  let paramsPresent = Object.keys(params);
  const index = paramsPresent.indexOf('groupBy'); //Elimino groupBy de parámetros presentes porque no representa un WHERE
  if (index > -1) {
    paramsPresent.splice(index, 1);
  }
  let addedString = "";

  if(paramsPresent.length > 0 && paramsPresent.every(v => whereParameters.includes(v))){
    addedString = "WHERE ";

    paramsPresent.forEach(function(elem) {
      if (elem == 'agrupacion')
        addedString += "agrupacion = '" + params[elem].toUpperCase() + "' AND ";
      else
        addedString += elem + " = " + params[elem] + " AND ";
    });

    //Borrar ultimo and
    addedString = addedString.slice(0, -4);
    
    return addedString;
  }
  if (paramsPresent.length > 0) //Mandaron params pero no los que tomamos
    return 'error';
  return '';
}

// -------------------------------------------------------------------------

const getVotos = async (request, response) => {

  const {error} = validateVotosParams(request.query); 
  if(error){
   //400 Bad Request
   return res.status(400).send(generateError(error.details[0].message));
  }

  let groupByPresent = request.query.groupBy != undefined;

  let queryString = "SELECT * FROM votos ";
  if (groupByPresent)
    queryString = "SELECT " + request.query.groupBy + ", SUM(votos) as votos FROM votos "

  //Agrego joins si necesito información que no está en la tabla votos
  if ((groupByPresent && request.query.groupBy.toLowerCase() == "agrupacion") || request.query.agrupacion != undefined)
    queryString += "NATURAL JOIN agrupaciones ";
  if ((groupByPresent && request.query.groupBy.toLowerCase() == "iddistrito") || request.query.iddistrito != undefined)
    queryString += "NATURAL JOIN mesas NATURAL JOIN secciones ";
  else if ((groupByPresent && request.query.groupBy.toLowerCase() == "idseccion") || request.query.idseccion != undefined)
    queryString += "NATURAL JOIN mesas ";
  
  //parseo
  let whereString = parseWhere(request.query);
  if (whereString == 'error'){
    response.status(400).send({
      message: 'Parámetros inválidos'
    });
    return;
  }

  queryString += whereString
  if (groupByPresent != undefined)
    queryString += "GROUP BY " + request.query.groupBy;

  queryString += ";"

  //console.log(queryString);

  pool.query(queryString, undefined, async(error, results) => {
    if (results != undefined)
      response.status(200).json(results.rows);
    else
      response.status(200).json([]);
  });
};

const getCargos = async (request, response) => {

  let queryString = "SELECT * FROM cargos ";
  if (request.params.id != undefined){
    queryString += "WHERE idcargo = " + request.params.id;
  }
  queryString += ";"


  pool.query(queryString, undefined, async(error, results) => {
    if (results != undefined)
      response.status(200).json(results.rows);
    else
      response.status(200).json([]);
  });
};

const getCargosForDistrict = async (request, response) => {
  if (request.params.id == undefined){
    response.status(400).send({
      message: 'No se especificó el id del distrito'
    });
    return;
  }

  let schema = { 
    id: Joi.number().min(0),
  };       
  if (!Joi.validate(request.params,schema)){
    response.status(400).send({
      message: 'El id del distrito debe ser un número positivo'
    });
    return;
  }

  let queryString = "SELECT DISTINCT cargo, idcargo FROM cargos NATURAL JOIN votos NATURAL JOIN mesas NATURAL JOIN " +
    "secciones WHERE iddistrito = " + request.params.id + ";";

  pool.query(queryString, undefined, async(error, results) => {
    if (results != undefined)
      response.status(200).json(results.rows);
    else
      response.status(200).json([]);
  });
};

const getAgrupaciones = async (request, response) => {

  let queryString = "SELECT * FROM agrupaciones ";
  if (request.params.nombre != undefined){
    queryString += "WHERE agrupacion = '" + request.params.nombre.toUpperCase() + "'";
  }
  queryString += ";"

  pool.query(queryString, undefined, async(error, results) => {
    if (results != undefined)
      response.status(200).json(results.rows);
    else
      response.status(200).json([]);
  });
};

const getMesas = async (request, response) => {

  let queryString = "SELECT * FROM mesas ";
  if (request.params.id != undefined){
    queryString += "WHERE idmesa = " + request.params.id;
  }
  queryString += ";"


  pool.query(queryString, undefined, async(error, results) => {
    if (results != undefined)
      response.status(200).json(results.rows);
    else
      response.status(200).json([]);
  });
};

const getSecciones = async (request, response) => {

  let queryString = "SELECT * FROM secciones ";
  if (request.params.id != undefined){
    queryString += "WHERE idseccion = " + request.params.id;
  }
  queryString += ";"


  pool.query(queryString, undefined, async(error, results) => {
    if (results != undefined)
      response.status(200).json(results.rows);
    else
      response.status(200).json([]);
  });
};

const getDistritos = async (request, response) => {

  let queryString = "SELECT * FROM distritos ";
  if (request.params.id != undefined){
    queryString += "WHERE iddistrito = " + request.params.id;
  }
  queryString += ";"


  pool.query(queryString, undefined, async(error, results) => {
    if (results != undefined)
      response.status(200).json(results.rows);
    else
      response.status(200).json([]);
  });
};

const getTiposVoto = async (request, response) => {
  
  let queryString = "SELECT * FROM tipovoto ";
  if (request.params.id != undefined){
    queryString += "WHERE idtipo = " + request.params.id;
  }
  queryString += ";"


  pool.query(queryString, undefined, async(error, results) => {
    if (results != undefined)
      response.status(200).json(results.rows);
    else
      response.status(200).json([]);
  });
};

const getAgrupationPercentagesPerSection = async (request, response) => {
  const idcargo = request.query.idcargo;
  const iddistrito = request.query.iddistrito;

  if (idcargo == undefined || iddistrito == undefined){
    response.status(400).send({
      message: 'Parámetro idcargo o iddistrito no especificado'
    });
    return;
  }

  const queryString = "SELECT agrupacion, seccion, 100 * SUM(votos) / totalSeccion::float as porcentaje " +
                      "FROM votos NATURAL JOIN agrupaciones NATURAL JOIN mesas NATURAL JOIN secciones NATURAL JOIN ( " +
                        "SELECT iddistrito, seccion, SUM(votos) as totalSeccion " +
                        "FROM votos NATURAL JOIN mesas NATURAL JOIN secciones " +
                        "WHERE iddistrito = " + iddistrito + " AND idcargo = " + idcargo + " AND idagrupacion <> 0 " +
                        "GROUP BY seccion, iddistrito " +
                        ") as aux " +
                      "WHERE iddistrito = " + iddistrito + " AND idcargo = " + idcargo + " AND idagrupacion <> 0 " +
                      "GROUP BY agrupacion, seccion, totalSeccion;";

                    
  pool.query(queryString, undefined, async(error, results) => {
    if (results != undefined){
      let answer = [];
      results.rows.forEach(element => {
        answer.push({agrupacion: element.agrupacion, seccion: (element.seccion), porcentaje: parseFloat(element.porcentaje).toFixed(2)});
      });
      response.status(200).json(answer);
    }
    else
      response.status(200).json([]);
  });
};

const getNonPositive = async (request, response) => {
  let distrito = request.query.distrito;
  if(distrito == null) {
    distrito = "%";
  }
  const queryString = "SELECT distrito, seccion, tipo, votos "+
                      "FROM votos NATURAL JOIN mesas NATURAL JOIN secciones NATURAL JOIN distritos NATURAL JOIN tipovoto " +
                      "WHERE distrito LIKE $1 AND idcargo=3 AND tipo IN ('nulos', 'recurridos', 'blancos', 'impugnados');"

  pool.query(queryString, [distrito], (error, results) => {
    response.status(200).json(results.rows);
  });
};

const getVotesMultipleParams = async (request, response) => {
  let cargo = request.query.cargo;
  let distrito = request.query.distrito;
  if(cargo == null) {
    cargo = "%";
  }
  if(distrito == null) {
    distrito = "%";
  }

  const queryString = "SELECT distrito, seccion, votos, agrupacion "+
                      "FROM votos NATURAL JOIN mesas NATURAL JOIN secciones NATURAL JOIN distritos NATURAL JOIN cargos NATURAL JOIN agrupaciones " +
                      "WHERE cargo LIKE $1 AND distrito LIKE $2 ;";


  pool.query(queryString, [cargo, distrito], (error, results) => {
    response.status(200).json(results.rows);
  });
};

const getVotesForPosition = async (request, response) => {
  let cargo = request.query.cargo;
  if(cargo == null) {
    cargo = "%";
  }
  const queryString = "SELECT distrito, seccion, votos "+
                      "FROM votos NATURAL JOIN mesas NATURAL JOIN secciones NATURAL JOIN distritos NATURAL JOIN cargos " +
                      "WHERE cargo LIKE $1 ";

  pool.query(queryString, [cargo], (error, results) => {
    response.status(200).json(results.rows);
  });
};

const getDate = async (request, response) => {
  const idcargo = request.query.idcargo;
  const iddistrito = request.query.iddistrito;

  if (idcargo == undefined || iddistrito == undefined){
    response.status(400).send({
      message: 'Parámetro idcargo o iddistrito no especificado'
    });
    return;
  }

  const queryString = "SELECT agrupacion, SUM(votos) as votos, fecha " +
                      "FROM public.votos NATURAL JOIN public.agrupaciones NATURAL JOIN public.mesas NATURAL JOIN public.secciones " +
                      "WHERE iddistrito = " + iddistrito + " AND idcargo = " + idcargo + " AND idagrupacion <> 0 " +
                      "GROUP BY fecha, agrupacion ";

                    
  pool.query(queryString, undefined, async(error, results) => {
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

const getType = async (request, response) => {
  const idcargo = request.query.idcargo;
  const iddistrito = request.query.iddistrito;

  if (idcargo == undefined || iddistrito == undefined){
    response.status(400).send({
      message: 'Parámetro idcargo o iddistrito no especificado'
    });
    return;
  }

  const queryString = "SELECT tipo, SUM(votos) as votos " +
                      "FROM public.votos NATURAL JOIN public.agrupaciones NATURAL JOIN public.mesas NATURAL JOIN public.secciones NATURAL JOIN public.tipovoto " +
                      "WHERE iddistrito = " + iddistrito + " AND idcargo = " + idcargo + " " +
                      "GROUP BY tipo ";

                    
  pool.query(queryString, undefined, async(error, results) => {
    if (results != undefined){
      let answer = [];
      results.rows.forEach(element => {
        answer.push({tipo: element.tipo, votos: parseInt(element.votos)});
      });
      response.status(200).json(answer);
    }
    else
      response.status(200).json([]);
  });
};

const getElectorsAndVotes = async (request, response) => {
  let distrito = request.query.distrito;
  
  const queryString = "SELECT votos, seccion, mesa, electores "+
                      "FROM votos NATURAL JOIN mesas NATURAL JOIN cargos NATURAL JOIN secciones NATURAL JOIN distritos " +
                      "WHERE cargo LIKE 'DIPUTADOS NACIONALES' AND distrito='" + distrito + "'";

  console.log(queryString)
  pool.query(queryString, (error, results) => {
    response.status(200).json(results.rows);
  });
};


module.exports = {
  getVotos,
  getAgrupaciones,
  getCargos,
  getCargosForDistrict,
  getMesas,
  getDistritos,
  getSecciones,
  getTiposVoto,
  getAgrupationPercentagesPerSection,
  getNonPositive,
  getVotesMultipleParams,
  getVotesForPosition,
  getDate,
  getType,
  getElectorsAndVotes
}
