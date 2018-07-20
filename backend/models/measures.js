import mongoose from 'mongoose';
const Schema = mongoose.Schema;

// create new instance of the mongoose.schema. the schema takes an
// object that shows the shape of your database entries.
const MeasuresSchema = new Schema({
  author: String,
  text: String,
});

// export our module to use in server.js
export default mongoose.model('Measure', MeasuresSchema);
