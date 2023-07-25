import React, { useState } from 'react';
import classes from './Authorization.module.css';
import axios from 'axios';

function Authorization(props) {

  const [login, setlogin] = useState('')
  function sendEmailAutho() {
    axios.post('/auth/login', { email: login }).then((response) => {
      console.log(response.data.data)
      if (response.data.data === 'Вход выполнен успешно') {
        props.authorization.authorize(login)
      }
    })
  }

  const onClickEnter = () => {
    sendEmailAutho()
  }

  const onChangeLogin = (e) => {
    setlogin(e.target.value)
  } 

  return (
    <div className={classes.authoriaion_content}>
      <div className={classes.authoriaion_header}>Войти</div>
      <input className={classes.authoriaion_input_item} placeholder='Логин' onChange={(e) => onChangeLogin(e)}></input>
      <button className={classes.authoriaion_enter} onClick={onClickEnter}>Вход</button>
    </div>
  );
}

export default Authorization;
