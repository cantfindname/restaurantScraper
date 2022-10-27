
const mysql = require('mysql2');
const express = require('express');
const bodyParser = require('body-parser');
require('dotenv').config();

var app = express();
app.use(bodyParser.json());

const pool = mysql.createPool({
    host : 'localhost',
    user : 'root',
    password : 'scrapy123=',
    database : 'restaurant',
    multipleStatements : true
});

// module.exports = pool.promise();


// app.get("/", (req,res)=>{
    //     pool.getConnection((err, connection)=> {
        //         if (err) throw err;
        //         console.log("connected as id " + connection.threadId);
        //         connection.query('select * from restaurant.restaurant_info', (err, res)=> {
            //             connection.release();
            //             if (err) throw err; 
            //             console.log('the data: /n', res);
            //         })
            //     })
            //     return res; 
            // })
            
app.get('/api/get', (req, res)=>{            
    let sql = 'select * from restaurant.restaurant_info where zipcode = 32601'
    pool.query(sql, (err, queryRes)=>{
        res.json(queryRes);
    });
});


app.listen(3001, ()=>{
    console.log("running on port 3001");
});