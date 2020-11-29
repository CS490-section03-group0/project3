import React, { useState, useEffect } from 'react';
import {
  Paper, makeStyles, Typography, CircularProgress,
} from '@material-ui/core';
import 'fontsource-roboto';
import { Link } from 'react-router-dom';

const useStyles = makeStyles(() => ({
  root: {
    flexGrow: 1,
    backgroundColor: '#f7cea2',
    borderStyle: 'solid',
    borderWidth: '3px',
    width: '70%',
    textAlign: 'center',
    margin: 'auto',
  },
  table: {
    textAlign: 'center',
    margin: 'auto',
  },
}));

type Transaction = {
  balance: number;
  id: number;
  name: string;
};

type LeaderboardData = {
  transactions: Array<Transaction>;
};

function Leaderboard() {
  const [transactions, setTransactions] = useState<Array<Transaction>>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/leaderboard')
      .then((res) => res.json())
      .then((data: LeaderboardData) => {
        setTransactions(data.transactions);
        setLoading(false);
      });
  }, []);

  const classes = useStyles();
  return (
    <div className="Leaderboard">
      <Paper className={classes.root} style={{ position: 'relative', top: '10vh' }} elevation={3}>
        <Typography variant="h3">
          Leaderboard
        </Typography>
        <br />
        <br />
        <img src="https://media3.giphy.com/media/3Gm15eZOsNk0tptIuG/giphy.gif" alt="coinflip" className="coinflipgif" style={{ height: '200px', width: '200px', borderRadius: '25px' }} />
        <br />
        <br />
        <table className={classes.table}>
          <Typography variant="h6">
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Balance</th>
            </tr>
            {loading ? <CircularProgress color="secondary" /> : null}
            {transactions.map((transaction) => (
              <tr>
                <td><Link to={`/profile/${transaction.id}`}>{transaction.id}</Link></td>
                <td><Link to={`/profile/${transaction.id}`}>{transaction.name}</Link></td>
                <td>{transaction.balance}</td>
              </tr>
            ))}
          </Typography>
        </table>

        <br />
      </Paper>
    </div>
  );
}

export default Leaderboard;