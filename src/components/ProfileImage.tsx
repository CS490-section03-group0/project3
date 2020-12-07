import React, { Dispatch, useState } from 'react';
import './ProfileImage.css';
import {
  Button, Typography, TextField,
} from '@material-ui/core';
import { useDispatch } from 'react-redux';
import { MessageActions, ADD_MESSAGE } from '../actions/messageActions';

interface Props {
  valid: boolean,
}

function ProfileImage(props: Props) {
  const { valid } = props;
  const [imageURL, setImageURL] = useState('');
  const messagesDispatch = useDispatch<Dispatch<MessageActions>>();
  const [imageMessage, setImageMessage] = useState('');

  function HandleFileChange(event) {
    setImageURL(event.target.value);
  }

  function HandleError() {
    setImageMessage('Bad Image');
  }

  function HandleLoad() {
    setImageMessage('');
  }

  function SubmitFile() {
    fetch('/api/settings/profilepic', {
      method: 'POST',
      headers: new Headers({ 'content-type': 'application/json' }),
      mode: 'no-cors',
      body: JSON.stringify({
        image_url: imageURL,
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
        <Typography variant="h6">Change Profile Picture</Typography>
        <TextField
          color="primary"
          variant="outlined"
          size="small"
          defaultValue={imageURL}
          onChange={HandleFileChange}
        />
        <Button color="primary" variant="contained" onClick={SubmitFile}>Confirm</Button>
        { imageURL !== ''
          ? (
            <div className="preview">
              <img id="preview" onError={HandleError} onLoad={HandleLoad} src={imageURL} alt="preview" />
              <div>{imageMessage}</div>
            </div>
          )
          : (
            null
          )}
      </div>
    );
  }
  return <div />;
}

export default ProfileImage;
