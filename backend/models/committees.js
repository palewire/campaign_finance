import mongoose from 'mongoose';
const Schema = mongoose.Schema;

const CommitteesSchema = new Schema({
  "_id": Schema.Types.ObjectId,
  "committee_id": String,
  "election_cycle": Number,
  "historical_names": [ String ],
  "status": String,
  "reporting_period": String,
  "current_contributions": String,
  "year_contributions": String,
  "current_expenditures": String,
  "year_expenditures": String,
  "ending_cash": String,
});

export default mongoose.model('Committees', CommitteesSchema);
