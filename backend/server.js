import express from 'express';
import bodyParser from 'body-parser';
import logger from 'morgan';
import mongoose from 'mongoose';
import { getSecret } from './secrets';
// import Comment from './models/comment'; // Exampel to import db entry

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

// TODO: Get and post to database example
// router.get('/comments', (req, res) => {
//   Comment.find((err, comments) => {
//     if (err) return res.json({ success: false, error: err });
//     return res.json({ success: true, data: comments });
//   });
// });
//
// router.post('/comments', (req, res) => {
//   const comment = new Comment();
//   // body parser lets us use the req.body
//   const { author, text } = req.body;
//   if (!author || !text) {
//     // we should throw an error. we can do this check on the front end
//     return res.json({
//       success: false,
//       error: 'You must provide an author and comment'
//     });
//   }
//   comment.author = author;
//   comment.text = text;
//   comment.save(err => {
//     if (err) return res.json({ success: false, error: err });
//     return res.json({ success: true });
//   });
// });
