var http = require('http');

var url = require('url');

var querystring = require('querystring');


var server = http.createServer(function(request,response){

    response.writeHead(200,{'Content-Type' : 'text/ html'});
    response.end('Hellow node.js!!');
});

server.listen(8080, function(){
    console.log('Server is running....');
});