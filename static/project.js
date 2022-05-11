const sqlite3 = require('sqlite3').verbose();
const express = require('express');
let app = express();
const pug = require("pug");

// open the database
let db = new sqlite3.Database('movies.db', (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to the movies database.');
});
// var db = new sqlite3.Database('movies.db');
module.exports = db;
// db.serialize(() => {
//   db.each(`SELECT movie as movie,
//                   streamer as streamer
//                   id as id
//            FROM streamers`, (err, row) => {
//     if (err) {
//       console.error(err.message);
//     }
//     console.log(row.movie + "\t" + row.streamer + "\t" + row.id);
//   });
// });






// db.close((err) => {
//   if (err) {
//     console.error(err.message);
//   }
//   console.log('Close the database connection.');
// });