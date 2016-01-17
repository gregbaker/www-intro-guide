var http = require('http');
var server = http.createServer(function(req, res) {
  res.setHeader('Content-type', 'text/html')
  res.writeHead(200);
  res.write('<!DOCTYPE html>\n');
  res.write('<html><head><meta charset="UTF-8" />\n');
  res.write('<title>Node.js app</title></head><body>\n');
  res.write('<p>This is a page generated by Node.js.\n');
  res.write('</p>\n');
  res.write('</body></html>\n');
  res.end();
});
server.listen(8080);