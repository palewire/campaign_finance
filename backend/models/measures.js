import mongoose from 'mongoose';
const Schema = mongoose.Schema;

const MeasuresSchema = new Schema({
  "_id": Schema.Types.ObjectId,
  "measure_name": String,
  "measure_id": Number,
  "supporting_committees": [{
    "committee_name": String,
    "committee_id": Number,
  }],
  "opposing_committees": [{
    "committee_name": String,
    "committee_id": Number,
  }],
}, {collection: "ballot_measures"});

export default mongoose.model('Measure', MeasuresSchema);
