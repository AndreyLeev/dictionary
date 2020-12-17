import React from 'react';
import {
  withStyles,
  Card,
  CardContent,
  CardActions,
  Modal,
  Button,
  TextField,
  Switch,
  FormControlLabel
} from '@material-ui/core';
import { compose } from 'recompose';
import { withRouter } from 'react-router-dom';
import { Form, Field } from 'react-final-form';

const styles = theme => ({
  modal: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  modalCard: {
    width: '90%',
    maxWidth: 1000,
  },
  modalCardContent: {
    display: 'flex',
    flexDirection: 'column',
  },
  marginTop: {
    marginTop: theme.spacing(2),
  },
});


// TODO add is_tagged_text boolean flag to payload


class TextEditor extends React.Component {
    constructor(props){
        super(props);
        this.state = {
             tagged_text : false
        }
        this.handleTextTypeInputChange = this.handleTextTypeInputChange.bind(this)
    }

    handleTextTypeInputChange(event) {
      this.setState({tagged_text: !this.state.tagged_text});
    }

    render() {
        return(
            <Form initialValues={this.props.text} onSubmit={this.props.onSave(
                    {"is_tagged_text": this.state.tagged_text}
                )}>
              {({ handleSubmit }) => (
                <Modal
                  className={this.props.classes.modal}
                  onClose={() => this.props.history.goBack()}
                  open
                >
                  <Card className={this.props.classes.modalCard}>
                    <form onSubmit={handleSubmit}>
                      <CardContent className={this.props.classes.modalCardContent}>
                        <Field name="title">
                          {({ input }) => <TextField label="Title" autoFocus {...input} />}
                        </Field>
                        {this.state.tagged_text?
                            <Field name="tagged_text">
                              {({ input }) => (
                                <TextField
                                  className={this.props.classes.marginTop}
                                  label="Tagged Text"
                                  multiline
                                  rows={15}
                                  {...input}
                                />
                              )}
                            </Field> :
                             <Field name="text">
                               {({ input }) => (
                                 <TextField
                                   className={this.props.classes.marginTop}
                                   label="Text"
                                   multiline
                                   rows={15}
                                   {...input}
                                 />
                               )}
                             </Field>
                         }
                      </CardContent>
                      <CardActions>
                        <Button size="small" color="primary" type="submit">Save</Button>
                        <Button size="small" onClick={() => this.props.history.goBack()}>Cancel</Button>
                        <FormControlLabel
                        control={
                            <Switch
                             checked={this.state.tagged_text}
                             onChange={this.handleTextTypeInputChange}
                             name="checkedA"
                             inputProps={{ 'aria-label': 'secondary checkbox' }}
                           />
                        }
                        label="Tagged Text"
                      />
                      </CardActions>
                    </form>
                  </Card>
                </Modal>
              )}
            </Form>
        );
    }
}


export default compose(
  withRouter,
  withStyles(styles),
)(TextEditor);
