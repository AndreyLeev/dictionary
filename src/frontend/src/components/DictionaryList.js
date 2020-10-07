import 'bootstrap/dist/css/bootstrap.min.css'
import React from 'react'
import { withRouter, Route, Redirect, Link } from 'react-router-dom';

import Card from 'react-bootstrap/Card'
import CardColumns from 'react-bootstrap/CardColumns'

import ListGroup from 'react-bootstrap/ListGroup'
import ListGroupItem from 'react-bootstrap/ListGroupItem'
import { compose } from 'recompose'
import { find } from 'lodash';

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


import Common from './common/Common'
import DictionaryEditor from './DictionaryEditor'
import ErrorSnackbar from './ErrorSnackbar'


const APP_API = process.env.APP_API || 'http://127.0.0.1:8000/api/';


const styles = theme => ({
  fab: {
    position: 'absolute',
    bottom: theme.spacing(3),
    right: theme.spacing(3),
    [theme.breakpoints.down('xs')]: {
      bottom: theme.spacing(2),
      right: theme.spacing(2),
    },
  },
});


class DictionaryManager extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        loading: true,
        dictionaries: [],
        error: null,
    };
  }

  componentDidMount() {
    this.getDictionaries();
  }

  async fetch(method, endpoint, body) {
      try {
        const response = await fetch(`${APP_API}${endpoint}`, {
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

  async getDictionaries() {
      this.setState(
          {
              loading: false,
              dictionaries: (await this.fetch('get', 'dictionaries/')) || []
          });
    }

   saveDictionary = async (dictionary) => {
      if (dictionary.id) {
        await this.fetch('put', `dictionaries/${dictionary.id}/`, dictionary);
      } else {
        await this.fetch('post', 'dictionaries/', dictionary);
      }

      this.props.history.goBack();
      this.getDictionaries();
  }

   async deleteDictionary(dictionary) {
       await this.fetch('delete', `dictionaries/${dictionary.id}/`);
       this.getDictionaries();
    }

  renderDictionaryEditor = ({ match: { params: { id } } }) => {
      if (this.state.loading) return null;
      const dictionary = find(this.state.dictionaries, { id: Number(id) });

      if (!dictionary && id !== 'new') return <Redirect to="/" />;

      return <DictionaryEditor dictionary={dictionary} onSave={this.saveDictionary} />;
    };

  render() {
    const { classes } = this.props;
    return (
        <Common>
            <CardColumns>{
             this.state.dictionaries.map((item) =>
               <Card
                   id={item.id}
                   className="text-center"
                   border="info"
                   style={{width: '18rem'}}
                    >
                 <Card.Body>
                   <Card.Title
                       class="text-primary">
                       <h3>{item.title}</h3>
                   </Card.Title >
                   <Card.Text>
                       {item.description}
                   </Card.Text>
                   <ListGroup className="list-group-flush">
                       <ListGroupItem>
                           Total words: {item.total_tokens || 0}
                       </ListGroupItem>
                       <ListGroupItem>
                           Total unique words: {item.total_unique_tokens || 0}
                       </ListGroupItem>
                       <ListGroupItem>
                           <small className="text-muted">
                               Created at {new Intl.DateTimeFormat("en-GB", {
                                 year: "numeric",
                                 month: "long",
                                 day: "2-digit"
                               }).format(new Date(item.creation_date))}
                           </small>
                       </ListGroupItem>
                    </ListGroup>
                 </Card.Body>
                 <Card.Footer>
                   <IconButton
                        onClick={() => this.deleteDictionary(item)} color="inherit"
                        >
                       <DeleteIcon color="secondary"/>
                   </IconButton>
                   <IconButton
                        key={item.id}
                        component={Link}
                        to={`/dictionaries/${item.id}`}
                       >
                       <EditIcon color="primary"/>
                   </IconButton>
                   <IconButton
                        key={item.id}
                        component={Link}
                        to={`/dictionary-details/${item.id}`}
                       >
                       <ArrowForwardIosIcon color="primary"/>
                   </IconButton>
                 </Card.Footer>
               </Card>
             )}
            </CardColumns>
            <Fab
          size="medium"
          color="secondary"
          aria-label="add"
          className={classes.fab}
          component={Link}
          to="/dictionaries/new"
        >
          <AddIcon />
        </Fab>
        <Route path="/dictionaries/:id" render={this.renderDictionaryEditor} />
        {this.state.error && (
          <ErrorSnackbar
            onClose={() => this.setState({ error: null })}
            message={this.state.error.message}
          />
        )}
        </Common>
    );
  }
}

export default compose(
  withRouter,
  withStyles(styles),
)(DictionaryManager);
