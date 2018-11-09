var _data = require('./data')
var handlers = {};

// Not-Found
handlers.notFound = function(data,callback){
  callback(404);
};

// Users
handlers.jsons = function(data,callback){
  var acceptableMethods = ['get'];
  if(acceptableMethods.indexOf(data.method) > -1){
    handlers._jsons[data.method](data,callback);
  } else {
    callback(405);
  }
};

handlers._jsons  = {};

handlers._jsons.get = function(data,callback){
  // Check that file is valid
  var file = typeof(data.queryStringObject.file) == 'string' && data.queryStringObject.file.trim().length > 0 ? data.queryStringObject.file.trim() : false;
  console.log(data)
  if(file){
    // Lookup the json
    _data.read('jsons',file,function(err,data){
      if(!err && data){
        callback(200, data);
      } else {
        callback(404);
      }
    });
  } else {
    callback(400,{'Error' : 'Missing required field'})
  }
};

module.exports = handlers;