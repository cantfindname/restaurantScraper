
const mysql = require('mysql2');
const express = require('express');
const bodyParser = require('body-parser');
require('dotenv').config();

var app = express();
app.use(bodyParser.json());


var mysqlConnection = mysql.createConnection({
    host : 'localhost',
    user : 'root',
    password : 'scrapy123=',
    database : 'restaurant',
    multipleStatements : true

});

mysqlConnection.connect((err) => {
    if (!err){
        console.log("Connected");
    }
    else{
        console.log("Connection Failed");
        console.log(err)
    }
})

app.listen(3000);