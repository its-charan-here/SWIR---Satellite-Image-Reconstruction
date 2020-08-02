// Entry point of the website
// The nodeJS file that will get our server started 
//Website will operate on localhost:3000
//flag==1 means that the generative inpainting method was selected
//flag==2 means that jpg or png image is uploaded
//flag==3 means that the OpenCV method was selected
//flag==4 means that tif image is uploaded 

var express=require("express");
var app=express();
var path = require('path');
var multer = require('multer');
var upload = multer({ dest: 'uploads/' });

var fs = require("fs");

// console.log(path.extname('index.html'));

let {PythonShell} = require('python-shell');

const spawn = require('child_process').spawn;

var bodyparser=require("body-parser");

app.use(bodyparser.urlencoded({extended:true}));



app.use(express.static(__dirname+"/public"));
app.use(express.static(__dirname+"/fonts"));
app.use(express.static(__dirname+"/generative_inpainting"));
app.use(express.static(__dirname+"/views"));
app.use(express.static(__dirname+"/uploads"));



app.set("view engine","ejs");

app.get("/",function(req,res){
    res.render("index");
});
var names;
app.post('/uploadFile', upload.single('file'), function(req,res) {
  // const file = req.file
  // if (!file) {
  //   const error = new Error('Please upload a file')
  //   error.httpStatusCode = 400
  //   return next(error)
  // }
  //   res.send(file)
  // document.getElementById("sub").style.display="none"; 
  var flag;
  var file=req.file;
   names=file.originalname;
  console.log(names);
  const tempPath = req.file.path;
  ex=path.extname(file.originalname);
  if (ex===".tif"){
    const targetPath = path.join(__dirname, "./uploads/image.tif");
    fs.rename(tempPath, targetPath, err => {
      if (err) return handleError(err, res);});
      flag=4;
      console.log("Calling python fucntion");
      const process = spawn('python', ['tif_to_jpg.py']);
          process.stdout.on('data', (data) => {
          console.log(data.toString());
          res.render("upload",{flag:flag,names:names});
      });
      
  }
  else{
    const targetPath = path.join(__dirname, "./uploads/image.jpg");
    fs.rename(tempPath, targetPath, err => {
      if (err) return handleError(err, res);

      console.log("done");
       flag=2;
  const file=req.file;
  ex=path.extname(file.originalname);
  if (ex===".rl0"){
    res.render("popup");
    
    console.log(flag);
  }
  
      
     res.render("upload",{flag:flag,names:names});
      
     
      //  res
      //  .status(200)
      //  .contentType("text/plain")
      //  .end();
    });
  }
  
});

app.post('/popup',function(req,res){
  var flag=2;
console.log(req.body.width);
console.log(req.body.height);
res.render("upload",{flag:flag});
});
// var storage = multer.diskStorage({
//   destination: function (req, file, cb) {
//     cb(null, 'uploads')
//   },
//   filename: function (req, file, cb) {
//     cb(null, file.fieldname + '-' + Date.now())
//   }
// })
 
// var upload = multer({ storage: storage })

app.get('/name', function (req, res) { 

  console.log("Calling python fucntion");
  const process = spawn('python', ['generative_inpainting/test.py']);

  process.stdout.on('data', (data) => {
      console.log(data.toString());
  });

  res.render("index");
});
  
// save code as start.js 

app.get('/run', function (req, res) {
    const subprocess = runScript()
    res.set('Content-Type', 'text/plain');
    subprocess.stdout.pipe(res)
    subprocess.stderr.pipe(res)
  });

app.get("/upload",function(req,res){
  var flag=0;
res.render("upload",{flag:flag});
});

app.post("/upload",function(req,res){

 var flag=1;

// console.log("Calling python fucntion");
//   const process = spawn('python', ['generative_inpainting/test.py']);

//   process.stdout.on('data', (data) => {
//       console.log(data.toString());

      res.render("upload",{flag:flag}); 
  // });

  
});
app.post("/upload1",function(req,res){

  var flag=1;
  
  console.log("Calling python fucntion");
    const process = spawn('python', ['generative_inpainting/test.py']);
  
    process.stdout.on('data', (data) => {
        console.log(data.toString());
        res.render("upload",{flag:flag,names:names}); 
   
    });

    process.on('close', (code) => {
      console.log(`child process close all stdio with code ${code}`);
      // send data to browser
      
      });
        });

  app.post("/upload2",function(req,res){
    var flag =3;
    console.log("button2 was pressed");
    console.log("Calling python fucntion");
    // const process = spawn('python', ['opencv_inpaint.py']);
    const process = spawn('python', ['cv_test.py']);
    
    process.stdout.on('data', (data) => {
        console.log(data.toString());
         res.render("upload",{flag:flag,names:names});
    });
  
    process.on('close', (code) => {
      console.log(`child process close all stdio with code ${code}`);
      // send data to browser
      
      });
  });

  // app.post("/upload3",function(req,res){
  //   var flag =1;
  //   console.log("button3 was pressed");
  //   res.render("upload",{flag:flag});
  //     });



var port = process.env.PORT || 3000;
app.listen(port, function () {
  console.log("Server Has Started!");
});