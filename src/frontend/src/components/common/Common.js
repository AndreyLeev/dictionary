import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { CssBaseline, Container, Paper } from '@material-ui/core'

import Bar from './Bar';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  appBarSpacer: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    height: '100vh',
    overflow: 'auto',
  },
  container: {
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4),
    paddingLeft: theme.spacing(20),
    paddingRight: theme.spacing(20),
  },
  paper: {
    padding: theme.spacing(2),
    display: 'flex',
    overflow: 'auto',
    flexDirection: 'column',
  },
}));

export default function (props) {
  const classes = useStyles();
  return (
    <div className={classes.root}>
      <CssBaseline />
      <Bar />
      <main className={classes.content}>
        <div className={classes.appBarSpacer} />
        <Container maxWidth="lg" className={classes.container}>
	  <Paper className={classes.paper}>
	    {props.children}
	  </Paper>
        </Container>
      </main>
    </div>
  );
}
