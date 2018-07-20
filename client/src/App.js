import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import {
  Icon,
  Intent,
  Spinner,
  Card,
  Button,
  FormGroup,
  Label,
  Menu,
  MenuItem,
  MenuDivider,
  Navbar,
  Alignment
} from '@blueprintjs/core';

import { Table, Column, Cell } from '@blueprintjs/table';
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
      </div>
    );
  }
}

export default App;
