import classes from './ProductCard.module.css';
import axios from 'axios';

function ProductCard(props) {

  const onClickPlus = () => {
    axios.patch('/basket/', {action: '+', card_id: props.card_id}).then((responce) => {
      props.changeBasket({action: '+', id: props.card_id})
      console.log(props.name + " добавлен в корзину");   
    })
  }

  const onClickMinus = () => {
    axios.patch('/basket/', {action: '-', card_id: props.card_id}).then((responce) => {
      props.changeBasket({action: '-', id: props.card_id})
      console.log(props.name + " удален из корзины");
    })
  }

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
          <button onClick={onClickMinus}>-</button>
          <div>{props.quantity}</div>
          <button onClick={onClickPlus}>+</button>
        </div>
      </div>
      <div className={classes.card_button_delete}>
        x
      </div>
    </div>
  );
}

export default ProductCard;
