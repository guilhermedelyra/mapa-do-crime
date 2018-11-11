/*
 * Library for storing and editing data
 *
 */

// Dependencies
var fs = require('fs');
var path = require('path');
var helpers = require('./helpers');

// Container for module (to be exported)
var lib = {};

// Base directory of data folder
lib.baseDir = path.join(__dirname,'/../.data/');


// Read data from a file
lib.read_json = function(dir,file,callback){
  fs.readFile(lib.baseDir+dir+'/'+file+'.json', 'utf8', function(err,data){
    if(!err && data){
      var parsedData = helpers.parseJsonToObject(data);
      callback(false,parsedData);
    } else {
      callback(err,data);
    }
  });
};

lib.read_img = function(dir,file,callback){
  fs.readFile(lib.baseDir+dir+'/'+file+'.png', function(err,data){
    if(!err && data){
      callback(false,data);
    } else {
      callback(err,data);
    }
  });
};

// Export the module
module.exports = lib;
