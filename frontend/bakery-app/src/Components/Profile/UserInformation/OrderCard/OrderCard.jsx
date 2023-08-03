import { useEffect, useState } from 'react';
import classes from './OrderCard.module.css';

function OrderCard(props) {
  



  return (
    <div className={classes.card_container}>
      <div className={classes.card_information}>
        <div className={classes.card_up_info}>
          <div className={classes.card_date}>
            Дата, время
          </div>
          <div className={classes.card_price}>
            1000
          </div>
        </div>
      </div>
      <div className={classes.card_status_and_actions}>
        <div className={classes.card_status}>
          Завершён
        </div>
        <div className={classes.card_actions}>
          <button>Повторить</button>
        </div>
      </div>
    </div>
  );
}

export default OrderCard;
