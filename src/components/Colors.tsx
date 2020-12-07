import React, { Dispatch, useState } from 'react';
import {
  Button, Typography,
} from '@material-ui/core';
import { useDispatch } from 'react-redux';
import { MessageActions, ADD_MESSAGE } from '../actions/messageActions';

type Color = {
  item_type: number,
  name: string,
};

interface Props {
  colors: Array<Color>,
}

function Colors(props: Props) {
  const { colors } = props;
  const [curColor, setCurColor] = useState('');
  const messagesDispatch = useDispatch<Dispatch<MessageActions>>();

  function HandleColorChange(event) {
    setCurColor(event.target.value);
  }

  function SubmitColor() {
    fetch('/api/settings/textcolor', {
      method: 'POST',
      headers: new Headers({ 'content-type': 'application/json' }),
      mode: 'no-cors',
      body: JSON.stringify({
        item_type: curColor,
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

  return (
    <div>
      { colors.length !== 0
        ? (
          <div>
            <Typography variant="h6">Change Text Color</Typography>
            <select onChange={HandleColorChange}>
              {colors.map((color) => (
                <option key={color.item_type} value={color.item_type}>{color.name}</option>
              ))}
            </select>
            <Button color="primary" value="Confirm" onClick={SubmitColor}>Confirm</Button>
          </div>
        )
        : (
          <div />
        )}
    </div>
  );
}

export default Colors;
