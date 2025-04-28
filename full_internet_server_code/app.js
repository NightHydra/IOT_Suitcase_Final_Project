const express = require('express');
const session = require('express-session');
const bcrypt = require('bcrypt');
const fs = require('fs');
const readline = require('readline');
const path = require('path');
const https = require('https');
const ndjson = require('express-json');

const app = express();
const port = 3000;

app.use(express.static('files_to_serve'))

app.use(ndjson())

// Load users from JSON
function loadUsers() {
  const data = fs.readFileSync(path.join(__dirname, 'user_data/users.json'));
  return JSON.parse(data);
}

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));


app.use(session({
  secret: 'super-secret-key', // In production, use a secure, env-stored key
  resave: false,
  saveUninitialized: false,
  cookie: { secure: true } // Set to true if using HTTPS
}));

app.post('/login', async (req, res) => {
  
  const users = loadUsers()
  const { username, password } = req.body;

  if (!users[username]) {
    console.log("Invlaid uname")
    return res.status(401).send('INVALID CREDENTIALS');
  }

  const match = await bcrypt.compare(password, users[username]);
  if (!match) {
    console.log("Bad password")
    return res.status(401).send('INVALID CREDENTIALS');
  }

  console.log("Logged user in")

  req.session.username = username;
  res.send('LOGGED IN');
});

// GET /images
app.get('/images', (req, res) => {
  const username = req.session.username;

  if (!username) {
    return res.status(403).send('FORBIDDEN');
  }

  if (!req.session.seenFiles) {
    req.session.seenFiles = new Set();
  }

  const seenFiles = new Set(req.session.seenFiles);
  const imagesDir = path.join(__dirname, 'files_to_serve', username, 'images');
  console.log(imagesDir)

  fs.readdir(imagesDir, (err, files) => {
      if (err) return res.status(500).send('Unable to read image folder' + imagesDir);
      imageFiles = files.filter(file => /\.(jpg|jpeg|png|gif)$/i.test(file));
    
      const newFiles = imageFiles.filter(file => !seenFiles.has(file));

      newFiles.forEach(file => seenFiles.add(file));
      console.log(newFiles)
      req.session.seenFiles = Array.from(seenFiles);
  
      res.json(newFiles);
    });
});

// GET /events
app.get('/events', (req, res) => {
    const username = req.session.username;

    /*
    if (!username) {
      return res.status(403).send('FORBIDDEN');
    }
    */
    filePath = path.join(__dirname, 'files_to_serve', 'alice', 'events', 'sensor_events.ndjson')

    if (!req.session.lastPosition) {
      req.session.lastPosition = 0;
    }
  
    fs.stat(filePath, (err, stats) => {
      if (err) return res.status(500).send('File error');
  
      const fileSize = stats.size;
  
      if (fileSize <= req.session.lastPosition) {
        console.log("NO DATA LEFT")
        return res.send('NA');
      }
  
      const stream = fs.createReadStream(filePath, {
        start: req.session.lastPosition,
        end: fileSize - 1, // inclusive
        encoding: 'utf8'
      });
  
      let data = '';
  
      stream.on('data', chunk => {
        data += chunk + "\n";
      });
  
      stream.on('end', () => {
        req.session.lastPosition = fileSize;
        res.send(data);
      });
  
      stream.on('error', (err) => {
        console.error(err);
        res.status(500).send('Stream error');
      });
    });
});

app.post("/images", (req, res) => {

  const username = req.session.username;

  if (!username) {
    return res.status(403).send('FORBIDDEN');
  }
  
  const { filename } = req.body;
  const safeName = path.basename(filename); // prevent path traversal
  const filePath = path.join(__dirname, 'files_to_serve', username, 'images', safeName);

  if (!fs.existsSync(filePath)) {
    console.log("FILE NOT FOUND")
    return res.status(404).send('File not found');
  }

  res.sendFile(filePath);
})



const options = {
  key: fs.readFileSync("certs/iotsuitcase_co.key"),                  //Change Private Key Path here
  cert: fs.readFileSync("certs/iotsuitcase_co.cert"),            //Change Main Certificate Path here          //Change Intermediate Certificate Path here
  };

https.createServer(options, app).listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})


