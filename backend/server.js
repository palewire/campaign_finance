import express from 'express';
import bodyParser from 'body-parser';
import logger from 'morgan';
import mongoose from 'mongoose';
import { getSecret } from './secrets';
import Measure from './models/measures';

// and create our instances
const app = express();
const router = express.Router();

const API_PORT = process.env.API_PORT || 3001; // either port 3001 or environment variable
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(logger('dev'));

router.get('/', (req, res) => {
  res.json({ message: 'Hello, World!' });
});

app.use('/api', router);
app.listen(API_PORT, () => console.log(`Listening on port ${API_PORT}`));

// db config
mongoose.connect(getSecret('dbUri'));
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));
