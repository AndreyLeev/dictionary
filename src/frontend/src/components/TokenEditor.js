import React from 'react';
import {
  withStyles,
  Card,
  CardContent,
  CardActions,
  Modal,
  Button,
  TextField,

  IconButton,
  List,
  ListItem,
  ListItemSecondaryAction,
  ListItemText,
  Typography,
} from '@material-ui/core';
import { compose } from 'recompose';
import { withRouter, Link } from 'react-router-dom';
import { Form, Field } from 'react-final-form';
import {
     ArrowForwardIos as ArrowForwardIosIcon,
} from '@material-ui/icons';




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


const TokenEditor = ({ classes, token, onSave, history, tokenTexts }) => (
  <Form initialValues={token} onSubmit={onSave}>
    {({ handleSubmit }) => (
      <Modal
        className={classes.modal}
        onClose={() => history.goBack()}
        open
      >
        <Card className={classes.modalCard}>
          <form onSubmit={handleSubmit}>
            <CardContent className={classes.modalCardContent}>
              <Field name="label">
                {({ input }) => <TextField label="Label" autoFocus {...input} />}
              </Field>
              <div>
                  <Typography variant="h6" className={classes.title}>
                    {tokenTexts.length ? 'Word texts' : null}
                  </Typography>
                  <List>
                      {tokenTexts.map((item) =>
                       <ListItem>
                           <ListItemText
                             primary={item.text_title}
                             secondary={'Total: ' + item.token_total}
                           />
                           <ListItemSecondaryAction>
                               <IconButton
                                key={item.text_id}
                                component={Link}
                                to={`/dictionary-details/${item.dictionary}/texts/${item.text_id}`}
                               >
                                   <ArrowForwardIosIcon color="primary"/>
                               </IconButton>
                           </ListItemSecondaryAction>
                       </ListItem>
                    )}
                  </List>
          </div>
            </CardContent>
            <CardActions>
              <Button size="small" color="primary" type="submit">Save</Button>
              <Button size="small" onClick={() => history.goBack()}>Cancel</Button>
            </CardActions>
          </form>
        </Card>
      </Modal>
    )}
  </Form>
);

export default compose(
  withRouter,
  withStyles(styles),
)(TokenEditor);
