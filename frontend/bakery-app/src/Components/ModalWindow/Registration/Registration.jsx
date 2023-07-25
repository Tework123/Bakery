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
    <div className={classes.pincode_content}>
      <div className={classes.pincode_header}>Введите код</div>
      <div className={classes.pincode_inputs}>
        <input className={classes.pincode_input_item}/>
        <input className={classes.pincode_input_item}/>
        <input className={classes.pincode_input_item}/>
        <input className={classes.pincode_input_item}/>
        <input
          name='code'
          type='hidden'
          className={classes.pincode_input_hidden}
          onChange={(e) => onChangeLogin(e)}/>
      </div>
      <div>Прислать код ещё раз</div>
    </div>
  );
}

export default Registration;
