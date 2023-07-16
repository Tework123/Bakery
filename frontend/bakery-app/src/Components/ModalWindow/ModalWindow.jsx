import React from 'react';
import classes from './ModalWindow.module.css';
import Authorization from './Authorization/Authorization';

function ModalWindow(props) {

  const authorizationModal = (
    <Authorization authorization={props.authorization}/>
  )

  // const registrationModal = (
  //   <Registration/>
  // )

  let modalChangableWindow; 


  const eventHandlerClickWhite = (e) => {
    e.stopPropagation();
  }

  return (
    <div className={classes.gray_container} onClick={props.closeModalWindow}>
      <div className={classes.white_background_content} onClick={(e) => eventHandlerClickWhite(e)}>
      <button className={classes.close_button} onClick={props.closeModalWindow}>x</button>
        {authorizationModal}

      </div>
    </div>
  );
}

export default ModalWindow;
