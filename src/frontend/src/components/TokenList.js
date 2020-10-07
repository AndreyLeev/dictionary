import React from 'react'
import MUIDataTable from "mui-datatables";

import TableToolbar from "./common/TableToolbar";
import {
     Edit as EditIcon,
} from '@material-ui/icons';
import {
  IconButton,
} from '@material-ui/core';


const APP_API = process.env.APP_API || 'http://127.0.0.1:8000/api/';


export default class TokenList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {tokens: []};
  }

  componentDidMount() {
    this.TokenList();
  }

  TokenList() {
    fetch(`${APP_API}dictionaries/${this.props.match.params.dictionaryId}/tokens/`)
      .then(res => res.json())
      .then((results) => this.setState({ tokens: results }))
  }

  render() {
    const columns = [
        "label",
        "frequency",
    ];
    const options = {
      filter: true,
      selectableRows: 'multiple',
      filterType: 'textField',
      responsive: 'vertical',
      rowsPerPage: 50,
    };
    return (
        <MUIDataTable
          title={"Tokens"}
          data={this.state.tokens}
          columns={columns}
          options={options}
        />
    );
  }
}
