import React from 'react'
import MUIDataTable from "mui-datatables";
import { withRouter, Route, Redirect, Link } from 'react-router-dom';

import { find } from 'lodash';
import { compose } from 'recompose'

import {
  IconButton,
} from '@material-ui/core';

import {
     Delete as DeleteIcon,
     Edit as EditIcon,
} from '@material-ui/icons';

import TextEditor from './TextEditor'
import TableToolbar from "./common/TableToolbar";
import DropFiles from './common/DropZone'

const APP_API = process.env.APP_API || 'http://127.0.0.1:8000/api/';


class TextList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        loading: true,
        texts: [],
        errors: null,
    };
  }

  componentDidMount() {
    this.getTexts();
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

  async getTexts() {
      this.setState(
          {
              loading: false,
              texts: (await this.fetch('get', 'texts/')) || []
          });
    }

   saveText = (tagged_text) => async (text) => {
      let paylaod = Object.assign({}, text, tagged_text);
      if (text.id) {
        await this.fetch('put', `texts/${text.id}/`, paylaod);
      } else {
        await this.fetch('post', 'texts/', paylaod);
      }

      this.props.history.goBack();
      this.getTexts();
  }

   async deleteText(textId) {
       await this.fetch('delete', `texts/${textId}/`);
       this.getTexts();
    }

  renderTextEditor = ({match}) => {
      const id = match.params.textId
      if (this.state.loading) return null;
      const text = find(this.state.texts, { id: Number(id) });

      if (!text && id !== 'new') return <Redirect to="/" />;
      return <TextEditor text={text} onSave={this.saveText} />;
    };

  render() {
    const columns = [
        {
           name: "id",
           options: {
             display: false,
           }
        },
        {
          name: "title",
          label: "Title",
        },
        {
          name: "creation_date",
          label: "Creation date",
          options: {
            filter: true,
            sort: true,
            empty: true,
            customBodyRender: (value, tableMeta, updateValue) => {
                console.log(tableMeta.rowData);
              return (
                  new Intl.DateTimeFormat("en-GB", {
                    year: "numeric",
                    month: "long",
                    day: "2-digit"
                }).format(new Date(tableMeta.rowData[2]))
              );
            }
          }
        },
        {
          name: "total_tokens",
          label: "Total words",
        },
        {
          name: "total_unique_tokens",
          label: "Total unique words",
        },
        {
          name: "Edit",
          label: "",
          options: {
            filter: true,
            sort: false,
            empty: true,
            customBodyRender: (value, tableMeta, updateValue) => {
              return (
                <IconButton
                     key={tableMeta.rowIndex}
                     component={Link}
                     to={`${this.props.match.url}/texts/${tableMeta.rowData[0]}`}
                    >
                    <EditIcon color="primary"/>
                </IconButton>
              );
            }
          }
        },
        {
          name: "Delete",
          label: "",
          options: {
            filter: true,
            sort: false,
            empty: true,
            customBodyRender: (value, tableMeta, updateValue) => {
              return (
                  <IconButton
                       onClick={() => this.deleteText(tableMeta.rowData[0])} color="inherit"
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
          <TableToolbar redirectLink={`${this.props.match.url}/texts/new`}/>
        );
      },
    };
    return (
        <div>
        <div>
            <DropFiles dictionaryId={this.props.match.params.dictionaryId}/>
        </div>
            <MUIDataTable
              title={"Texts"}
              data={this.state.texts}
              columns={columns}
              options={options}
            />
        <Route
            path="/dictionary-details/:dictionaryId/texts/:textId"
            render={this.renderTextEditor}
            />
    </div>
    );
  }
}


export default compose(
  withRouter,
)(TextList);
