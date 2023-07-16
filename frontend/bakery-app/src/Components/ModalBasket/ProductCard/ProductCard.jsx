import { useEffect, useState } from 'react';
import classes from './ProductCard.module.css';

function ProductCard(props) {

  return (
    <div className={classes.card_container}>
      <div className={classes.card_image}>
        <img />
      </div>
      <div className={classes.card_description}>
        <div className={classes.card_name}>
          {props.name}
        </div>
        <div className={classes.card_dop_text}>
          {props.description}
        </div>
        <div className={classes.card_price}>
          {props.price}
        </div>
        <div className={classes.card_button_add_delete}>
          <button>-</button>
          <div>{props.quantity}</div>
          <button>+</button>
        </div>
      </div>
      <div className={classes.card_button_delete}>
        x
      </div>
    </div>
  );
}

export default ProductCard;
