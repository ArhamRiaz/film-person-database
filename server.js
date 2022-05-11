// Create express app
const { response } = require("express");
var express = require("express")
var app = express()
var db = require("./static/project.js")
const pug = require("pug");

// Server port
var HTTP_PORT = 3000
// Start server
app.listen(3000);
console.log("Server listening at http://localhost:3000");

app.get("/api/users", (req, res) => {
    var sql = "select * from streamers"
    var params = []
    db.all(sql, params, (err, rows) => {
        if (err) {
          res.status(400).json({"error":err.message});
          return;
        }
        res.json({
            "message":"success",
            "data":rows
        })
      });
});

app.get("/movie/:id", (req, res) => {
    var sql = "select * from movies where title = ?"
    
    var params = [req.params.id]
    
    
    getStreaming(params, function(result){

      db.get(sql, params, (err, row) => {
        if (err) {
          res.status(400).json({"error":err.message});
          return;
        }
        console.log(sql,params);
        // console.log(result)
        let smash = result.split(",");
        let actors = row.actors.split(",");
        
        res.send(
            pug.renderFile("./pugfiles/moviePage.pug", {data: row, sites: smash, actors: actors})
        )
      });
    })
    
});

function getStreaming(title, callback){
  var sql2 = "select * from streamers where movie = ?"
  db.get(sql2, title, (err, row) =>{
    if (err) {
      res.status(400).json({"error":err.message});
      return;
    }

    // console.log("NEW DATA: " + row.streamer)
    callback(row.streamer);
  });

}




app.get("/movie", (req, res) => {
  var sql = "select * from movies where title = ?"
    
  var params = [req.query.movie]
  
  //let s = getStreaming(params);
  //console.log("what is s?" +s);
  
  getStreaming(params, function(result){

    db.get(sql, params, (err, row) => {
      if (err) {
        res.status(400).json({"error":err.message});
        return;
      }
      console.log(sql,params);
      // console.log(result)

      let smash = result.split(",");
      let actors = row.actors.split(",");
      
      res.send(
          pug.renderFile("./pugfiles/moviePage.pug", {data: row, sites: smash, actors:actors})
      )
    });
  })
  
});

app.get("/site", (req, res) => {
  var sql = "select * from sites where name = ?"
  var params = [req.query.site]
  db.get(sql, params, (err, row) => {
      if (err) {
        res.status(400).json({"error":err.message});
        return;
      }
      console.log(sql,params);
    
      let smash = row.movies.split(",")
      let num = smash.length
      //console.log(smash)
     
      
      res.send(
          pug.renderFile("./pugfiles/site.pug", {data: row, movies:smash, count:num})
      )
    });
});



app.get("/site/:id", (req, res) => {
  var sql = "select * from sites where name = ?"
  var params = [req.params.id]
  db.get(sql, params, (err, row) => {
      if (err) {
        res.status(400).json({"error":err.message});
        return;
      }
      console.log(sql,params);
    
      let smash = row.movies.split(",")
      let num = smash.length
      
      
      
      res.send(
          pug.renderFile("./pugfiles/site.pug", {data: row, movies:smash, count:num})
      )
    });
});

app.get("/director/:id", (req, res) => {
  var sql = "select * from directors where name = ?"
  var params = [req.params.id]
  db.get(sql, params, (err, row) => {
      if (err) {
        res.status(400).json({"error":err.message});
        return;
      }
      console.log(sql,params);
    
      let smash = row.movies.split(",")
      let num = smash.length
   
      
      res.send(
          pug.renderFile("./pugfiles/director.pug", {data: row, movies:smash, count:num})
      )
    });
});

app.get("/director", (req, res) => {
  var sql = "select * from directors where name = ?"
  var params = [req.query.director]
  db.get(sql, params, (err, row) => {
      if (err) {
        res.status(400).json({"error":err.message});
        return;
      }
      console.log(sql,params);
    
      let smash = row.movies.split(",")
      let num = smash.length
 
      
      res.send(
          pug.renderFile("./pugfiles/site.pug", {data: row, movies:smash, count:num})
      )
    });
});

app.get("/actor/:id", (req, res) => {
  var sql = "select * from actors where name = ?"
  var params = [req.params.id]
  db.get(sql, params, (err, row) => {
      if (err) {
        res.status(400).json({"error":err.message});
        return;
      }
      console.log(sql,params);
    
      let smash = row.movies.split(",")
      let num = smash.length
   
      
      res.send(
          pug.renderFile("./pugfiles/actor.pug", {data: row, movies:smash, count:num})
      )
    });
});

app.get("/actor", (req, res) => {
  var sql = "select * from actors where name = ?"
  var params = [req.query.actor]
  db.get(sql, params, (err, row) => {
      if (err) {
        res.status(400).json({"error":err.message});
        return;
      }
      console.log(sql,params);
    
      let smash = row.movies.split(",")
      let num = smash.length
 
      
      res.send(
          pug.renderFile("./pugfiles/actor.pug", {data: row, movies:smash, count:num})
      )
    });
});

app.get("/combo", (req, res) => {
  var sql = "select * from directors where name = ?"
  var params = [req.query.site]
  var director = [req.query.director]
  var movies_on_site = []
  db.get(sql, params, (err, row) => {
      if (err) {
        res.status(400).json({"error":err.message});
        return;
      }
      console.log(sql,params);
    
      let smash = row.movies.split(",")
      let num = smash.length
 
      
      res.send(
          pug.renderFile("./pugfiles/director.pug", {data: row, movies:smash, count:num})
      )
    });
});


// Root endpoint
app.get("/", (req, res) => {
    res.status(200);
    res.sendFile('./static/index.html', { root: __dirname });
    return;
});





// Default response for any other request
app.use(function(req, res){
    res.status(404);
});