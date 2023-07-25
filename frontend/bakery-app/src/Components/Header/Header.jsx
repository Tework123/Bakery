import React, { useEffect, useState } from 'react';
import classes from './Header.module.css';
import axios from 'axios';
import { NavLink } from 'react-router-dom';

function Header(props) {



  const onClickEnter = () => {
    props.changeTypeModalWindow(props.types.MODAL_AUTHORIZATION)
  }

  const onClickProfileTest = () => {
     
  }

  return (
    <header className={classes.header_container}>
      <div className={classes.header_main}>
        <div>Logo</div>
        <div>Телефон, адрес</div>
        <div className={classes.right_actions}>
          {props.isAuthorizated ?
          <NavLink
            to='/profile'>
            <div className={classes.item} onClick={onClickProfileTest}>
              Личный кабинет
            </div>
            </NavLink>
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
