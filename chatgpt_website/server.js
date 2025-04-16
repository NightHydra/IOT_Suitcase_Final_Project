const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.static('public'));
app.use(express.json());

// Serve the HTML page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

// API to get image list
app.get('/api/images', (req, res) => {
  const imagesDir = path.join(__dirname, 'public', 'images');
  fs.readdir(imagesDir, (err, files) => {
    if (err) return res.status(500).send('Unable to read image folder' + imagesDir);
    const imageFiles = files.filter(file => /\.(jpg|jpeg|png|gif)$/i.test(file));
    res.json(imageFiles);
  });
});

// API to get log content
app.get('/api/logs', (req, res) => {
  const logPath = path.join(__dirname, 'logs', 'app.log');
  fs.readFile(logPath, 'utf8', (err, data) => {
    if (err) return res.status(500).send('Log file not found');
    res.send(data);
  });
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});