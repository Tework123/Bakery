import classes from './ProductCard.module.css';

function ProductCard(props) {


  const onClickAddProduct = () => {
    props.addProduct(props.id)
  }

  return (
    <div className={classes.card_container}>
      <div className={classes.card_image}>
        <img alt='No image' src={props.imageURL}/>
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
          <button onClick={onClickAddProduct}>В корзину</button>
        </div>
      </footer>
    </div>
  );
}

export default ProductCard;
