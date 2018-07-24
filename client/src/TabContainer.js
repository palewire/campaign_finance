import React, { Component } from 'react';
import './TabContainer.css';

import {
  Icon,
  Alignment,
  Intent,
  Elevation,
  Tab,
  Tabs,
  Card,
  Button
} from '@blueprintjs/core';

import 'normalize.css/normalize.css';
import '@blueprintjs/core/lib/css/blueprint.css';
import '@blueprintjs/table/lib/css/table.css';

class TabContainer extends Component {
    render() {
      return (
        <div className="TabContainer">
            <Tabs id="TabsExample" onChange={this.handleTabChange} selectedTabId="ng">
                <Tab id="ng" title="Ballot Measures" panel={"Write panel info here"} />
                <Tab id="mb" title="Candidates" panel={"Write panel info here"} />
                <Tab id="rx" title="Independent Expenditures" panel={"Write panel info here"} />
                <Tabs.Expander />
                <input className="bp3-input" type="text" placeholder="Search..."/>
            </Tabs>
            <Card interactive={false} elevation={Elevation.TWO}>
                <h5><a href="#">Card heading</a></h5>
                <p>Card content</p>
                <Button>Submit</Button>
            </Card>
        </div>
      );
    }
}

export default TabContainer;
