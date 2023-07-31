import React from 'react';
import classes from './ModalWindow.module.css';
import Authorization from './Authorization/Authorization';
import Registration from './Registration/Registration';

function ModalWindow(props) {



  let email; 
  const giveEmail = (sendedEmail) => {
    email = sendedEmail
  }

  const authorizationModal = (
    <Authorization
      giveEmail={giveEmail}
      authorization={props.authorization}
      changeTypeModalWindow={props.changeTypeModalWindow}
      constTypesModal={{MODAL_REGISTRATION: props.types.MODAL_REGISTRATION}}/>
  )
  const registrationModal = (
    <Registration
      email={email}
      authorization={props.authorization}
      requestForSuccessfulRegistaration={props.functions.requestForSuccessfulRegistaration}
      changeTypeModalWindow={props.changeTypeModalWindow}
      constTypesModal={{MODAL_REGISTRATION: props.types.MODAL_AUTHORIZATION}}/>
  )

  let modalChangableWindow; 
  if (props.type === props.types.MODAL_REGISTRATION) {
    modalChangableWindow = registrationModal;
  } else if (props.type === props.types.MODAL_AUTHORIZATION){
    modalChangableWindow = authorizationModal
  }



  const eventHandlerClickWhite = (e) => {
    e.stopPropagation();
  }

  return (
    <div className={classes.gray_container} onClick={props.closeModalWindow}>
      <div className={classes.white_background_content} onClick={(e) => eventHandlerClickWhite(e)}>
      <button className={classes.close_button} onClick={props.closeModalWindow}>x</button>

        {modalChangableWindow}

      </div>
    </div>
  );
}

export default ModalWindow;
