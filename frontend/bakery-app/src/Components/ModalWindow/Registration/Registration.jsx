import React, { useState } from 'react';
import classes from './Registration.module.css';
import axios from 'axios';

function Registration(props) {

  
  const [login, setlogin] = useState('')
  function sendEmailRegistr() {
    axios.post('/auth/register', { email: login }).then((response) => {

      console.log(response.data.data)
      props.requestForSuccessfulRegistaration()
    })
  }




  const onClickRegistr = () => {
    sendEmailRegistr()
  }



  const onChangeLogin = (e) => {
    setlogin(e.target.value)
  } 

  const onChangePassword = () => {

  }


  return (
    <div className={classes.authoriaion_content}>
      <div className={classes.authoriaion_header}>Зарегистрироваться</div>
      <input className={classes.authoriaion_input_item} placeholder='Логин' onChange={(e) => onChangeLogin(e)}></input>
      <div className={classes.authoriaion_enter} onClick={onClickRegistr}>Зарегистрироваться</div>
      <div className={classes.authoriaion_old_account}>Уже есть аккаунт</div>
    </div>
  );
}

export default Registration;
