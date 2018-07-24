import React, { Component } from 'react';
import './App.css';
import TabContainer from './TabContainer';

import {
  Icon,
  Alignment,
  Intent, // Accent colors
  Spinner,
  Button,
  Elevation,
  Navbar
} from '@blueprintjs/core';

import 'normalize.css/normalize.css';
import '@blueprintjs/core/lib/css/blueprint.css';
import '@blueprintjs/table/lib/css/table.css';

class App extends Component {
  render() {
    return (
      <div className="App">
      <Navbar>
          <Navbar.Group align={Alignment.LEFT}>
              <Navbar.Heading>CALmatters</Navbar.Heading>
              <Navbar.Divider />
              <Button className="bp3-minimal" text="Home" />
              <Button className="bp3-minimal" text="About" />
              <Button className="bp3-minimal" text="Data" />
              <Button className="bp3-minimal" text="Docs" />
          </Navbar.Group>
      </Navbar>
      <TabContainer />
      </div>
    );
  }
}

export default App;
