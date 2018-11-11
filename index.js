/*
 * Primary file for API
 *
 */

// Dependencies
var http = require('http');
var url = require('url');
var StringDecoder = require('string_decoder').StringDecoder;
var handlers = require('./lib/handlers')
var helpers = require('./lib/helpers')
var config = require('./lib/config')
var fs = require('fs');

 // Instantiate the HTTP server
var httpServer = http.createServer(function(req,res){
  unifiedServer(req,res);
});

// Start the HTTP server
httpServer.listen(config.httpPort,function(){
  console.log('The HTTP server is running on port '+config.httpPort);
});


// All the server logic for both the http and https server
var unifiedServer = function(req,res){

  // Parse the url
  var parsedUrl = url.parse(req.url, true);

  // Get the path
  var path = parsedUrl.pathname;
  var trimmedPath = path.replace(/^\/+|\/+$/g, '');

  // Get the query string as an object
  var queryStringObject = parsedUrl.query;

  // Get the HTTP method
  var method = req.method.toLowerCase();

  //Get the headers as an object
  var headers = req.headers;

  // Get the payload,if any
  var decoder = new StringDecoder('utf-8');
  var buffer = '';
  req.on('data', function(data) {
      buffer += decoder.write(data);
  });
  req.on('end', function() {
      buffer += decoder.end();

      // Check the router for a matching path for a handler. If one is not found, use the notFound handler instead.
      var chosenHandler = typeof(router[trimmedPath]) !== 'undefined' ? router[trimmedPath] : handlers.notFound;

      // Construct the data object to send to the handler
      var data = {
        'trimmedPath' : trimmedPath,
        'queryStringObject' : queryStringObject,
        'method' : method,
        'headers' : headers,
        'payload' : helpers.parseJsonToObject(buffer)
      };

      // Route the request to the handler specified in the router
      chosenHandler(data,function(statusCode,payload){
        statusCode = typeof(statusCode) == 'number' ? statusCode : 200;
        payload = typeof(payload) == 'object'? payload : {};
        var head = 'image/png';
        if (statusCode != 201) {
            payload = JSON.stringify(payload);
            head = 'application/json';
        }

        // Return the response
        res.setHeader('contentType', head);
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.writeHead(statusCode);
        res.end(payload, 'binary');
        console.log(trimmedPath,statusCode);
      });

  });
};

// Define the request router
var router = {
    'jsons' : handlers.jsons,
    'imgs' : handlers.imgs
};
