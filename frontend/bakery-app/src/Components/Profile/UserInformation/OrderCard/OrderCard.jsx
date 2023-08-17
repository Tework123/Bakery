import { useEffect, useState } from 'react';
import classes from './OrderCard.module.css';

function OrderCard(props) {
  
  return (
    <div className={classes.card_container}>
      <div className={classes.card_information}>
        <div className={classes.card_up_info}>
          <div className={classes.card_date}>
            {props.order.date}
          </div>
          <div className={classes.card_price}>
           {props.order.price}
          </div>
        </div>
        <div className={classes.card_images}>
          {props.order.cards.map((card) => <img alt='No image' src={card.image} loading="lazy"/>)}
        </div>
      </div>
      <div className={classes.card_status_and_actions}>
        <div className={classes.card_status}>
          {props.order.status}
        </div>
        <div className={classes.card_actions}>
          <button>Повторить</button>
        </div>
      </div>
    </div>
  );
}

export default OrderCard;
