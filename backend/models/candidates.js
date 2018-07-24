import mongoose from 'mongoose';
const Schema = mongoose.Schema;

const CandidatesSchema = new Schema({
  "_id": Schema.Types.ObjectId,
  "candidate_id": Number,
  "candidate_name": String,
  "party": String,
  "spending_limits": String,
  "races": [{
    "office": String,
    "election": String,
    "result": String
  }],
  "committees": [{
    "committee_id": Number,
    "committee_name": String,
    "current_status": String,
    "last_report_date": String, // TODO: Format dates
    "reporting_period": String,
    "curr_contribs": String,
    "total_contribs": String,
    "total_contribs": String,
    "curr_expenditures": String,
    "total_expenditures": String,
    "ending_cash": String,
  }],
});

export default mongoose.model('Candidates', CandidatesSchema);
