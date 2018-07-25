import * as React from 'react';
import './DataTable.css';
import 'normalize.css/normalize.css';
import '@blueprintjs/core/lib/css/blueprint.css';
import '@blueprintjs/table/lib/css/table.css';
import 'react-virtualized/styles.css';
import {
  Column,
  Table,
  AutoSizer,
  SortDirection,
  SortIndicator
} from 'react-virtualized';
import 'react-virtualized/styles.css';

// TODO: Make interactive tables for each entry, also include function to export as CSV
// Make this a child of VizContainer
// Table example: https://github.com/bvaughn/react-virtualized/blob/master/source/Table/Table.example.js

const list = [
  { name: 'Brian Vaughn', description: 'Software engineer' },
  { name: 'Data 1', description: 'Software engineer' },
  { name: 'Data 2', description: 'Software engineer' }
];

class DataTable extends React.Component {
  render() {
    return (
      <Table
        width={300}
        height={300}
        headerHeight={20}
        rowHeight={30}
        rowCount={list.length}
        rowGetter={({ index }) => list[index]}
      >
        <Column
          label='Name'
          dataKey='name'
          width={100}
        />
        <Column
          width={200}
          label='Description'
          dataKey='description'
        />
      </Table>
    );
  }
}

export default DataTable;
