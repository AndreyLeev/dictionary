import React from 'react'
import MUIDataTable from "mui-datatables";
import { withRouter, Route, Redirect, Link } from 'react-router-dom';

import { compose } from 'recompose'
import { find } from 'lodash';

import {
     Edit as EditIcon,
     Delete as DeleteIcon,
} from '@material-ui/icons';
import {
  IconButton,
} from '@material-ui/core';


import TokenEditor from './TokenEditor'
import TableToolbar from "./common/TableToolbar";


const APP_API = process.env.APP_API || 'http://127.0.0.1:8000/api/';


class TokenList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        loading: true,
        tokens: [],
        errors: null,
    };
    this.tokenTexts = []
  }

  componentDidMount() {
    this.getTokens();
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

  async getTokens() {
      this.setState(
          {
              loading: false,
              tokens: (await this.fetch('get', 'tokens/')) || []
          });
    }

   saveToken = async (token) => {
      if (token.id) {
        await this.fetch('put', `tokens/${token.id}/`, token);
      } else {
        await this.fetch('post', 'tokens/', token);
      }

      this.props.history.goBack();
      this.getTokens();
  }

   async deleteToken(tokenId) {
       await this.fetch('delete', `tokens/${tokenId}/`);
       this.getTokens();
    }

    async getTokenTexts(method, token, body) {
        try {
          const response = await fetch(
              `${APP_API}texts/?dict_id=${token.dictionary}&token=${token.label}`,
            {
            method,
            body: body && JSON.stringify(body),
            headers: {
              'content-type': 'application/json',
              accept: 'application/json',
            },
          });
          this.tokenTexts = await response.json() || [];
        } catch (error) {
          console.error(error);

          this.setState({ error });
        }
    }

  renderTokenEditor = ({match}) => {
      const id = match.params.tokenId
      if (this.state.loading) return null;
      const token = find(this.state.tokens, { id: Number(id) });

      if (!token && id !== 'new') return <Redirect to="/" />;

      if (id !== 'new'){
          this.getTokenTexts('get', token)
      } else {
          this.tokenTexts = []
      }
      return <TokenEditor token={token} tokenTexts={this.tokenTexts} onSave={this.saveToken} />;
    };


  render() {
    const columns = [
        {
           name: "id",
           options: {
             display: false,
           }
        },
        "label",
        "frequency",
        {
          name: "Edit",
          options: {
            filter: true,
            sort: false,
            empty: true,
            customBodyRender: (value, tableMeta, updateValue) => {
              return (
                <IconButton
                     key={tableMeta.rowIndex}
                     component={Link}
                     to={`${this.props.match.url}/tokens/${tableMeta.rowData[0]}`}
                    >
                    <EditIcon color="primary"/>
                </IconButton>
              );
            }
          }
        },
        {
          name: "Delete",
          options: {
            filter: true,
            sort: false,
            empty: true,
            customBodyRender: (value, tableMeta, updateValue) => {
              return (
                  <IconButton
                       onClick={() => this.deleteToken(tableMeta.rowData[0])} color="inherit"
                       >
                      <DeleteIcon color="secondary"/>
                  </IconButton>
              );
            }
          }
        },
    ];
    const options = {
      filter: true,
      selectableRows: 'multiple',
      filterType: 'textField',
      responsive: 'vertical',
      rowsPerPage: 50,
      customToolbar: () => {
        return (
          <TableToolbar redirectLink={`${this.props.match.url}/tokens/new`}/>
        );
      },
    };
    return (
        <div>
            <MUIDataTable
              title={"Words"}
              data={this.state.tokens}
              columns={columns}
              options={options}
            />
            <Route
                path="/dictionary-details/:dictionaryId/tokens/:tokenId"
                render={this.renderTokenEditor}
                />
        </div>

    );
  }
}

export default compose(
  withRouter,
)(TokenList);
