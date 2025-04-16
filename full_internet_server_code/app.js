const express = require('express')
const fs = require('fs');
const path = require('path');

const app = express()
const port = 3000

app.use(express.static('files_to_serve'))
app.use(express.json());

app.get('/images', (req, res) => {
  const imagesDir = path.join(__dirname, 'files_to_serve/images');
  fs.readdir(imagesDir, (err, files) => {
      if (err) return res.status(500).send('Unable to read image folder' + imagesDir);
      const imageFiles = files.filter(file => /\.(jpg|jpeg|png|gif)$/i.test(file));
      res.json(imageFiles);
    });
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
