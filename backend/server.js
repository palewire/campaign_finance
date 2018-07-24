import express from 'express';
import mongoose from 'mongoose';
import { getSecret } from './secrets';
import Measure from './models/measures';
import Funds from './models/funds';
import Committees from './models/committees';
import Candidates from './models/candidates';

const app = express();
const router = express.Router();

const API_PORT = process.env.API_PORT || 3001; // either port 3001 or environment variable

// db config, MongoDB uri stored in secrets.js (not included in Github repo)
mongoose.connect(getSecret('dbUri'));

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));
db.once('open', () => {console.log("Connected to MongoDB");});

app.get('/', (req, res) => {
  res.send({ message: 'Hello, World!' });
});

app.get('/measures', (req,res) => {
  Measure.find((err, measures) => {
    if (err) return res.json({ success: false, error: err});
    return res.send({data: measures});
  });
});

app.get('/funds', (req,res) => {
  Funds.find((err, funds) => {
    if (err) return res.json({ success: false, error: err});
    return res.send({data: funds})
  });
});

app.get('/committees', (req,res) => {
  Committees.find((err, committees) => {
    if (err) return res.json({ success: false, error: err});
    return res.send({data: committees});
  });
});

app.get('/candidates', (req,res) => {
  Candidates.find((err, candidates) => {
    if (err) return res.json({ success: false, error: err});
    return res.send({data: candidates});
  })
});

app.listen(API_PORT, () => console.log("App listening on port 3001"));
