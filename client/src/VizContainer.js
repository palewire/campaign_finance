import * as React from 'react';
import axios from 'axios';
import './VizContainer.css';
import 'normalize.css/normalize.css';
import '@blueprintjs/core/lib/css/blueprint.css';
import '@blueprintjs/table/lib/css/table.css';
import DataTable from './DataTable';

// TODO: Clean up data and pass down state to DataTable and Viz

var measures = [];
var candidates = [];
var contribsReceived = [];
var contribsMade= [];
var expenditures = [];
var lateContribs = [];
var lateExpend = [];

axios.get('/measures') // Use Axios to get data from server
  .then((res) => {
    for (var i in res.data) {
      measures.push(i)
    }
    console.log(res.data);
  });

class VizContainer extends React.Component {
  render() {
    return (
      <div className="VizContainer">
        <DataTable />
      </div>
    );
  }
}

export default VizContainer;
