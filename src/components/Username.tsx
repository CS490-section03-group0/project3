import React, { Dispatch, useState } from 'react';
import {
  Button, Typography, TextField,
} from '@material-ui/core';
import { useDispatch } from 'react-redux';
import { MessageActions, ADD_MESSAGE } from '../actions/messageActions';

interface Props {
  valid: boolean,
}

function Username(props: Props) {
  const { valid } = props;
  const [username, setUsername] = useState('');
  const messagesDispatch = useDispatch<Dispatch<MessageActions>>();

  function HandleUsername(event) {
    setUsername(event.target.value);
  }

  function SubmitUsername() {
    const tusername = username;
    fetch('/api/settings/username', {
      method: 'POST',
      headers: new Headers({ 'content-type': 'application/json' }),
      mode: 'no-cors',
      body: JSON.stringify({
        username: tusername,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        messagesDispatch({
          type: ADD_MESSAGE,
          payload: {
            message: `${data.message}`,
            type: 'success',
          },
        });
      });
  }

  if (valid) {
    return (
      <div style={{ textAlign: 'center' }}>
        <Typography variant="h6">Change Username</Typography>
        <TextField
          color="primary"
          variant="outlined"
          size="small"
          defaultValue={username}
          onChange={HandleUsername}
        />
        <Button color="primary" variant="contained" onClick={SubmitUsername}>Confirm</Button>
      </div>
    );
  }
  return <div />;
}

export default Username;
