var express = require('express');
var path = require('path');
var index = require('./routes/index');
var news = require('./routes/news');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade');
app.use('/static',
    express.static(path.join(__dirname, '../client/build/static/')));

// TODO: remove this after development is done
app.all('*', function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  next();
});

app.use('/', index);
app.use('/news', news);

app.use(function(req, res, next) {
  res.status(404);
});

module.exports = app;
