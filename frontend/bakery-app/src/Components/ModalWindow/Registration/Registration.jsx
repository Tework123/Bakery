import React, { useState } from 'react';
import classes from './Registration.module.css';
import axios from 'axios';

function Registration(props) {

  
  const [pincode, setPincode] = useState()

  function sendPincodeToServer() {
    console.log(props.email);
    axios.post('/auth/login_code', { code: pincode, email: props.email }).then((response) => {
      console.log(response.data.data)
      props.authorization.authorize(props.email)
      props.changeTypeModalWindow('')
    })
  }


  

  const onChangeLogin = (e) => {
    setPincode(e.target.value)
  } 

  const focusStyle = {border: '0.6px solid rgba(0, 0, 0, 0.3)'}
  const simpleStyle = {border: '0.6px solid rgba(0, 0, 0, 1)'}


  return (
    <div className={classes.pincode_content}>
      <div className={classes.pincode_header}>Введите код</div>
      <div className={classes.pincode_inputs}>
        <input className={classes.pincode_input_item} style={focusStyle} onChange={(e) => onChangeLogin(e)}/>
        <input className={classes.pincode_input_item} style={focusStyle}/>
        <input className={classes.pincode_input_item} style={focusStyle}/>
        <input className={classes.pincode_input_item} style={focusStyle}/>
        <input
          name='code'
          type='hidden'
          className={classes.pincode_input_hidden}
          />
      </div>
      <div>Прислать код ещё раз</div>
      <button onClick={sendPincodeToServer}> ОТПРАВИТЬ КОД</button>
    </div>
  );
}

export default Registration;
