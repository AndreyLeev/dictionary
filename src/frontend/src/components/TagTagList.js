import React from 'react'
import MUIDataTable from "mui-datatables";
import { withRouter } from 'react-router-dom';

import { find } from 'lodash';
import { compose } from 'recompose'

import TableToolbar from "./common/TableToolbar";

const APP_API = process.env.APP_API || 'http://127.0.0.1:8000/api/';


class TagTagList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        loading: true,
        tags: [],
        errors: null,
    };
  }

  componentDidMount() {
    this.getTagTagList();
  }

  async fetch(method, endpoint, body) {
      try {
        const response = await fetch(
            `${APP_API}dictionaries/${this.props.match.params.dictionaryId}/${endpoint}`,
          {
          method,
          body: body && JSON.stringify(body),
          headers: {
            'content-type': 'application/json',
            accept: 'application/json',
          },
        });
        return await response.json();
      } catch (error) {
        console.error(error);

        this.setState({ error });
      }
  }

  async getTagTagList() {
      this.setState(
          {
              loading: false,
              tags: (await this.fetch('get', 'tags_tags/')) || []
          });
    }

  render() {
    const columns = [
        {
          name: "code_1",
          label: "Code 1",
        },
        {
          name: "code_2",
          label: "Code 2",
        },
        {
          name: "frequency",
          label: "Frequency",
        },
    ];

    const options = {
      filter: true,
      selectableRows: 'multiple',
      filterType: 'textField',
      responsive: 'vertical',
      rowsPerPage: 50,
    };
    return (
    <div>
        <MUIDataTable
          title={"Tags Pairs"}
          data={this.state.tags}
          columns={columns}
          options={options}
        />
    </div>
    );
  }
}


export default compose(
  withRouter,
)(TagTagList);
