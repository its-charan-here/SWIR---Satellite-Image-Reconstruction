// Entry point of the website
// The nodeJS file that will get our server started 
//Website will operate on localhost:3000
//flag==1 means that the generative inpainting method was selected
//flag==2 means that jpg or png image is uploaded
//flag==3 means that the OpenCV method was selected
//flag==4 means that tif image is uploaded 

var express=require("express");//package for web development framework
var app=express();
var path = require('path');//It provides a way of working with directories and file paths
var multer = require('multer');//middleware to upload files
var upload = multer({ dest: 'uploads/' });

var fs = require("fs");

// console.log(path.extname('index.html'));

let {PythonShell} = require('python-shell');//package to connect with python programs

const spawn = require('child_process').spawn;//package to connect with python programs

var bodyparser=require("body-parser");//package to get data from forms

app.use(bodyparser.urlencoded({extended:true}));


//The express package will explicity serve the following files
app.use(express.static(__dirname+"/public"));
app.use(express.static(__dirname+"/fonts"));
app.use(express.static(__dirname+"/generative_inpainting"));
app.use(express.static(__dirname+"/views"));
app.use(express.static(__dirname+"/uploads"));



app.set("view engine","ejs");//direct access/call to ejs files

app.get("/",function(req,res){
    res.render("index");//renders home page(index.ejs)
});
var names;//Is created to store and pass the actual name of image uploaded
app.post('/uploadFile', upload.single('file'), function(req,res) {//post request to submit image uploaded from device
  // const file = req.file
  // if (!file) {
  //   const error = new Error('Please upload a file')
  //   error.httpStatusCode = 400
  //   return next(error)
  // }
  //   res.send(file)
  // document.getElementById("sub").style.display="none"; 
  var flag;
  var file=req.file;//gets the file details
   names=file.originalname;//stores original name of file
  console.log(names);
  const tempPath = req.file.path;//stores file path
  ex=path.extname(file.originalname);//finds extension of image
  if (ex===".tif"){//checks for tif type image
    const targetPath = path.join(__dirname, "./uploads/image.tif");//stores image as image.tif in uploads folder
    fs.rename(tempPath, targetPath, err => {
      if (err) return handleError(err, res);});
      flag=4;
      console.log("Calling python fucntion");
      const process = spawn('python', ['tif_to_jpg.py']);//call to python function to convert tif image to jpg for displaying purpose
          process.stdout.on('data', (data) => {
          console.log(data.toString());
          res.render("upload",{flag:flag,names:names});//render the upload.ejs method to proceed further
      });
      
  }
  else{
    const targetPath = path.join(__dirname, "./uploads/image.jpg");//uploads jpg image in uploads folder
    fs.rename(tempPath, targetPath, err => {
      if (err) return handleError(err, res);

      console.log("done");
       flag=2;
  const file=req.file;
  ex=path.extname(file.originalname);
  if (ex===".rl0"){//checks for rl0 file
    res.render("popup");//calls popup.ejs
    
    console.log(flag);
  }
  
      
     res.render("upload",{flag:flag,names:names});//call the upload.ejs file
      
     
      //  res
      //  .status(200)
      //  .contentType("text/plain")
      //  .end();
    });
  }
  
});

app.post('/popup',function(req,res){//post request to get width and height by user
  var flag=2;
console.log(req.body.width);
console.log(req.body.height);
res.render("upload",{flag:flag});//call upload.ejs
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

app.get("/upload",function(req,res){//get request for /upload
  var flag=0;
res.render("upload",{flag:flag});//calls upload file for user to submit image
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
app.post("/upload1",function(req,res){//post request for generative inpainting

  var flag=1;
  
  console.log("Calling python fucntion");
    const process = spawn('python', ['generative_inpainting/test.py']);//calls the generative inpainting python file
  
    process.stdout.on('data', (data) => {//collects data from python file
        console.log(data.toString());
        res.render("upload",{flag:flag,names:names}); //calls upload.ejs
   
    });

    process.on('close', (code) => {//closes connection between node and python
      console.log(`child process close all stdio with code ${code}`);
      // send data to browser
      
      });
        });

  app.post("/upload2",function(req,res){//post request for openCV
    var flag =3;
    console.log("button2 was pressed");
    console.log("Calling python fucntion");
    // const process = spawn('python', ['opencv_inpaint.py']);
    const process = spawn('python', ['cv_test.py']);//calls the openCV prog here
    
    process.stdout.on('data', (data) => {
        console.log(data.toString());
         res.render("upload",{flag:flag,names:names});//calls upload.ejs
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


//website hosted on localhost:3000
var port = process.env.PORT || 3000;
app.listen(port, function () {
  console.log("Server Has Started!");
});