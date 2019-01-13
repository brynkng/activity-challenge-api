import React from 'react';
import Card from "@material-ui/core/Card";
import Table from "@material-ui/core/Table";
import TableRow from "@material-ui/core/es/TableRow/TableRow";
import TableCell from "@material-ui/core/es/TableCell/TableCell";
import {withStyles} from "@material-ui/core";
import Typography from "@material-ui/core/Typography";
import TableBody from "@material-ui/core/TableBody";
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';


const styles = theme => ({
    title: {
        margin: '.5em 0'
    },
    card: {
        paddingTop: '1.5em',
        margin: '1em 0',
    },
    table: {
        marginTop: '1em'
    }
});

class PointDisplay extends React.Component {
    state = {
        expanded: false
    };

    handleClick = () => {
        let expanded = this.state.expanded;
        this.setState({expanded: !expanded})
    };

    render() {
        const {classes} = this.props;

        return (
            <Card className={classes.card} onClick={this.handleClick}>
                <Typography variant="title">{this.props.name}</Typography>

                <Typography variant="inherit">
                    <Table className={this.props.classes.table}>
                        <TableBody>
                            <TableRow>
                                <TableCell>Total Points</TableCell>
                                <TableCell align="right"><Typography variant="display1">{this.props.point_details.points}</Typography></TableCell>
                            </TableRow>
                            {
                                this.state.expanded ?
                                    <>
                                        <TableRow>
                                            <TableCell>Active Minutes</TableCell>
                                            <TableCell>{this.props.point_details.active_minutes}</TableCell>
                                        </TableRow>
                                        <TableRow>
                                            <TableCell>Cardio Zone Minutes</TableCell>
                                            <TableCell>{this.props.point_details.cardio_zone_minutes}</TableCell>
                                        </TableRow>
                                        <TableRow>
                                            <TableCell>Peak Zone Minutes</TableCell>
                                            <TableCell>{this.props.point_details.peak_zone_minutes}</TableCell>
                                        </TableRow>
                                    </> :
                                    null
                            }

                        </TableBody>
                    </Table>
                </Typography>

                {!this.state.expanded ? <ExpandMoreIcon fontSize="large"/> : null}
            </Card>
        );
    }
}

export default withStyles(styles)(PointDisplay);