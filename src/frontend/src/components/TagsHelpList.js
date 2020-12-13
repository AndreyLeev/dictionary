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
import TagEditor from './TagEditor'
import TableToolbar from "./common/TableToolbar";

const APP_API = process.env.APP_API || 'http://127.0.0.1:8000/api/';


class TagsHelpList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        loading: true,
        tags: [],
        errors: null,
    };
  }

  componentDidMount() {
    this.getTagsHelpList();
  }

  async fetch(method, endpoint, body) {
      try {
        const response = await fetch(
            `${APP_API}${endpoint}`,
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

  async getTagsHelpList() {
      this.setState(
          {
              loading: false,
              tags: (await this.fetch('get', 'tags/')) || []
          });
    }

   saveTag = async (tag) => {
      if (tag.id) {
        await this.fetch('put', `tags/${tag.id}/`, tag);
      } else {
        await this.fetch('post', 'tags/', tag);
      }

      this.props.history.goBack();
      this.getTagsHelpList();
  }

   async deleteTag(tagId) {
       await this.fetch('delete', `tags/${tagId}/`);
       this.getTagsHelpList();
    }

  renderTagEditor = ({match}) => {
      console.log("bsasbasfafasfasfasdjkfhaskjfdhs")
      const id = match.params.tagId
      if (this.state.loading) return null;
      const tag = find(this.state.tags, { id: Number(id) });
      console.log(tag)

      if (!tag && id !== 'new') return <Redirect to="/" />;
      return <TagEditor tag={tag} onSave={this.saveTag} />;
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
          name: "code",
          label: "Code",
        },
        {
          name: "title",
          label: "Title",
        },
        {
          name: "frequency",
          label: "Frequency",
        },
        {
          name: "examples",
          label: "Examples",
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
                     to={`${this.props.match.url}/tags/${tableMeta.rowData[0]}`}
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
                       onClick={() => this.deleteTag(tableMeta.rowData[0])} color="inherit"
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
          <TableToolbar redirectLink={`${this.props.match.url}/tags/new`}/>
        );
      },
    };
    return (
    <div>
        <MUIDataTable
          title={"Tags Help"}
          data={this.state.tags}
          columns={columns}
          options={options}
        />
        <Route
            path="/dictionary-details/:dictionaryId/tags/:tagId"
            render={this.renderTagEditor}
            />
    </div>
    );
  }
}


export default compose(
  withRouter,
)(TagsHelpList);
