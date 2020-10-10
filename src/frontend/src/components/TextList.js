import React from 'react'
import MUIDataTable from "mui-datatables";
import { withRouter, Route, Redirect, Link } from 'react-router-dom';

import { find } from 'lodash';
import { compose } from 'recompose'

import {
  withStyles,
  Fab,
  IconButton,
} from '@material-ui/core';

import {
     Delete as DeleteIcon,
     Add as AddIcon,
     Edit as EditIcon,
     ArrowForwardIos as ArrowForwardIosIcon
} from '@material-ui/icons';

import TextEditor from './TextEditor'
import TableToolbar from "./common/TableToolbar";
import DictionaryList from './DictionaryList'


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

   saveText = async (text) => {
      if (text.id) {
        await this.fetch('put', `texts/${text.id}/`, text);
      } else {
        await this.fetch('post', 'texts/', text);
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
        "title",
        "creation_date",
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
