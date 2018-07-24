import * as React from 'react';
import './TabContainer.css';
import axios from 'axios';

import {
  Icon,
  Alignment,
  Intent,
  Elevation,
  Tab,
  Tabs,
  Card,
  Button,
  H3
} from '@blueprintjs/core';

import 'normalize.css/normalize.css';
import '@blueprintjs/core/lib/css/blueprint.css';
import '@blueprintjs/table/lib/css/table.css';

axios.get('/measures') // Use Axios to get data from server
  .then((res) => {
    console.log(res.data);
  });

const BallotMeasuresPanel: React.SFC<{}> = () => (
    <div>
        <H3>Ballot Measures Panel</H3>
        <Card interactive={false} elevation={Elevation.TWO}>
            <h5><a href="#">Card heading</a></h5>
            <p>Card content</p>
            <Button>Submit</Button>
        </Card>
    </div>
);

const CandidatesPanel: React.SFC<{}> = () => (
    <div>
      <H3>Candidates Panel</H3>
      <Card interactive={false} elevation={Elevation.TWO}>
          <h5><a href="#">Card heading</a></h5>
          <p>Card content</p>
          <Button>Submit</Button>
      </Card>
    </div>
);

const ExpendituresPanel: React.SFC<{}> = () => (
  <div>
    <H3>Independent Expenditures Panel</H3>
    <Card interactive={false} elevation={Elevation.TWO}>
        <h5><a href="#">Card heading</a></h5>
        <p>Card content</p>
        <Button>Submit</Button>
    </Card>
  </div>
);

// TODO: Write handleTabChange

class TabContainer extends React.Component {
    render() {
      return (
        <div className="TabContainer">
            <Tabs id="TabsExample" onChange={this.handleTabChange} selectedTabId="ng">
                <Tab id="ng" title="Ballot Measures" panel={<BallotMeasuresPanel/>} />
                <Tab id="mb" title="Candidates" panel={<CandidatesPanel/>} />
                <Tab id="rx" title="Independent Expenditures" panel={<ExpendituresPanel/>} />
                <Tabs.Expander />
                <input className="bp3-input" type="text" placeholder="Search..."/>
            </Tabs>
        </div>
      );
    }
}

export default TabContainer;
