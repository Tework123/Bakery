import classes from './ProductCard.module.css';

function ProductCard(props) {


  const onClickAddProduct = () => {
    props.addProduct(props.product)
  }

  return (
    <div className={classes.card_container}>
      <div className={classes.card_image}>
        <img alt='No image' src={props.product.image}/>
      </div>
      <div className={classes.card_name}>
        {props.product.name}
      </div>
      <div className={classes.card_description}>
        {props.product.description}
      </div>
      <footer className={classes.card_bottom_place}>
        <div className={classes.card_price}>
          {props.product.price}
        </div>
        <div className={classes.card_button__container}>
          <button onClick={onClickAddProduct}>В корзину</button>
        </div>
      </footer>
    </div>
  );
}

export default ProductCard;
