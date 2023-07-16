import classes from './ProductCard.module.css';

function ProductCard(props) {

  return (
    <div className={classes.card_container}>
      <div className={classes.card_image}>
        <img alt='Ну ничего страшного' src={props.imageURL}/>
      </div>
      <div className={classes.card_name}>
        {props.name}
      </div>
      <div className={classes.card_description}>
        {props.description}
      </div>
      <footer className={classes.card_bottom_place}>
        <div className={classes.card_price}>
          {props.price}
        </div>
        <div className={classes.card_button__container}>
          <button>В корзину</button>
        </div>
      </footer>
    </div>
  );
}

export default ProductCard;
