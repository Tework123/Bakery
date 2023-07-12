import React, { useEffect, useState } from 'react';
import classes from './Header.module.css';
import axios from 'axios';

function Header() {

  const [login, setlogin] = useState('')
  const [isAuthorithised, setIsAuthorithised] = useState(false)

  function sendEmailAutho() {
    axios.post('/auth/login', { login: login }).then((response) => {
      console.log(response.data.data)
      if (response.data.data === 'Вход выполнен успешно') {
        setIsAuthorithised(true)
      }
    })

  }

  function sendEmailRegistr() {
    axios.post('/auth/register', { login: login }).then((response) => {

      console.log(response.data.data)
      if (response.data.data === 'Регистрация прошла успешно') {
        setIsAuthorithised(true)
      }
    })

  }

  const changelogin = (e) => {
    setlogin(e.target.value)
  }

  return (
    <header className={classes.header_container}>
      <div className={classes.header_main}>
        <div>Logo</div>
        <div>Телефон, адрес</div>
        <div className={classes.right_actions}>
          {isAuthorithised ?
            <React.Fragment>
              <div className={classes.item}>
                Почта
              </div>
              <div className={classes.item} onClick={setIsAuthorithised(false)}>
                Выйти
              </div>
            </React.Fragment>
            :
            <React.Fragment><input placeholder='Почта' onChange={changelogin} value={login}></input>
              <div className={classes.item} onClick={sendEmailAutho}>
                Вход
              </div>
              <div className={classes.item} onClick={sendEmailRegistr}>
                Регистрация
              </div> </React.Fragment>
          }
        </div>
      </div>
    </header>
  );
}

export default Header;
