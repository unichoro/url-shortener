var http = require('http');
var querystring = require('querystring');

var server = http.createServer(function(request,response){
    var postdata = '';
    request.on('data', function(data) {
        postdata=postdata+data;
    });

    request.on('end', function() {
        var parsedQuery = querystring.parse(postdata);
        console.log(querystring);
        response.writeHead(200, {'Content-Type':'text/html'})
        response.end('value of val1='+ result);
    })
});

server.listen(8080, function(){
    console.log('Server is running....')
})