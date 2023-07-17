import React, { useEffect, useState } from 'react';
import classes from './Header.module.css';
import axios from 'axios';

function Header(props) {



  const onClickEnter = () => {
    props.changeTypeModalWindow(props.types.MODAL_AUTHORIZATION)
  }



  const onClickProfileTest = () => {
    axios.get('/profile').then((response) => {
      console.log(response.data);
    })   
  }

  return (
    <header className={classes.header_container}>
      <div className={classes.header_main}>
        <div>Logo</div>
        <div>Телефон, адрес</div>
        <div className={classes.right_actions}>
          {props.isAuthorizated ?
            <div className={classes.item} onClick={onClickProfileTest}>
              Личный кабинет
            </div>
            :
            <div className={classes.item} onClick={onClickEnter}>
              Вход
            </div>
          }
        </div>
      </div>
    </header>
  );
}

export default Header;
