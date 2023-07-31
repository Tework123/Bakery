import React, { useState } from 'react';
import classes from './Authorization.module.css';
import axios from 'axios';


function Authorization(props) {

  const [login, setlogin] = useState('')
  function sendEmailAutho() {
    axios.post('/auth/login', { email: login, credentials: 'include' }).then((response) => {
      console.log(response.data.data)
      if (response.data.data === 'Вход тестового работника выполнен успешно') {
        
        debugger
        props.authorization.authorize(login)
        props.changeTypeModalWindow('')
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
      <input className={classes.authoriaion_input_item} placeholder='Почта' onChange={(e) => onChangeLogin(e)}></input>
      <button className={classes.authoriaion_enter} onClick={onClickEnter}>Отправить пинкод на почту</button>
    </div>
  );
}

export default Authorization;
