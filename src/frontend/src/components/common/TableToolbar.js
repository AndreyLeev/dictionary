import React from "react";
import IconButton from "@material-ui/core/IconButton";
import Tooltip from "@material-ui/core/Tooltip";
import AddIcon from "@material-ui/icons/Add";
import { withStyles } from "@material-ui/core/styles";
import AttachFileIcon from '@material-ui/icons/AttachFile';

import { withRouter, Route, Redirect, Link } from 'react-router-dom';


const defaultToolbarStyles = {
  iconButton: {
  },
};

class CustomToolbar extends React.Component {

  handleClick = () => {
    console.log("clicked on icon!");
  }

  render() {
    const { classes } = this.props;

    return (
      <React.Fragment>
        <Tooltip title={"Add item"}>
          <IconButton
                className={classes.iconButton}
                onClick={this.handleClick}
                component={Link}
                to={this.props.redirectLink}
            >
            <AddIcon className={classes.deleteIcon} />
          </IconButton>
        </Tooltip>
      </React.Fragment>
    );
  }

}

export default withStyles(defaultToolbarStyles, { name: "CustomToolbar" })(CustomToolbar);
