
const mysql = require('mysql2')
const express = require('express')
const bodyParser = require('body-parser')
const axios = require('axios')

require('dotenv').config()

var app = express()
app.use(bodyParser.json())

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
        // let sql = 'select * from restaurant.restaurant_info where zipcode = 32601 limit 0, 10'
        let sql = `select * from restaurant_info as info
            inner join ta_info as ta
            on info.unique_id = ta.unique_id 
            inner join yelp_info as yelp
            on info.unique_id = yelp.unique_id limit 10
            `
        pool.query(sql, (err, queryRes)=>{
        res.json(queryRes);
    });
});

app.get('/search', (req, res)=>{
    // params[:keyword]
    console.log(req.query['keyword'])
    const searchKeyword = req.query['keyword']

    let sql = `SELECT * FROM restaurant_info WHERE name SOUNDS LIKE "${searchKeyword}" limit 10;`
    pool.query(sql, (err, searchRes)=>{
        res.json(searchRes)
    })
    // console.log('hi');
    // res.end();
    // send back data here! json: { data: {...}}
});


app.listen(3001, ()=>{
    console.log("running on port 3001");
});