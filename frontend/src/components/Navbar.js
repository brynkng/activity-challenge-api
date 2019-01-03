import React from 'react'
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import Typography from '@material-ui/core/Typography'
import Link from "react-router-dom/Link";
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
    link: {
        color: 'inherit',
        textDecoration: 'none',
        '&:hover': {color: 'inherit'}
    },
});

const NavBar = (props) => {
    const { classes } = props;
    return (
        <div>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="title" color="inherit">
                        <Link to="/" className={classes.link}>Activity Challenge</Link>
                    </Typography>
                </Toolbar>
            </AppBar>
        </div>
    )
}

export default withStyles(styles)(NavBar);