import React, { useState } from 'react';
import classes from './Authorization.module.css';
import axios from 'axios';


function Authorization(props) {

  const [email, setemail] = useState('')
  function sendEmailAutho() {
    axios.post('/auth/login', { email: email}).then((response) => {
      props.giveEmail(email)
      props.changeTypeModalWindow(props.constTypesModal.MODAL_REGISTRATION)
    })
  }


  const onClickEnter = () => {
    sendEmailAutho()
  }

  const onChangeEmail = (e) => {
    setemail(e.target.value)
  } 

  return (
    <div className={classes.authoriaion_content}>
      <div className={classes.authoriaion_header}>Войти</div>
      <input className={classes.authoriaion_input_item} placeholder='Почта' onChange={(e) => onChangeEmail(e)}></input>
      <button className={classes.authoriaion_enter} onClick={onClickEnter}>Отправить пинкод на почту</button>
      
    </div>
  );
}

export default Authorization;
