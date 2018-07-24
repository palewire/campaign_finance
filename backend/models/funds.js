import mongoose from 'mongoose';
const Schema = mongoose.Schema;

const FundsSchema = new Schema({
  "_id": Schema.Types.ObjectId,
  "committee_id": Number,
  "committee_name": String,
  "contributions": [{
    "contributor_names": [ String ],
    "payment_type": String,
    "city": String,
    "state": String,
    "contributor_id": Number,
    "employer": String,
    "occupation": String,
    "amount": String, // TODO: Format amounts
    "trans_date": String, // TODO: Format dates
    "field_date": String,
    "trans_no": Number,
  }],
  "expenditure": [{
    "date": String, // TODO: Format dates
    "payee": String,
    "expenditure_code": String,
    "description": String,
    "amount": String, //TODO: Format amounts
  }],
  "eletion_year": Number,
  "funding_type": String,
}, {collection: "funds"});

export default mongoose.model('Funds', FundsSchema);
