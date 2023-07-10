import { Fragment, useState } from 'react';
import classes from './ModalBasket.module.css';
import ProductCard from './ProductCard/ProductCard';

function ModalBasket(props) {

  console.log(props.isModalBasketOpen);

  let styleModalContainer;
  let styleModalWindow;

  if (props.isModalBasketOpen) {
    styleModalContainer = { display: 'flex' }
    styleModalWindow = {right: 0}
  } else {
    styleModalContainer = { display: 'none' }
    styleModalWindow = {right: 450}
  }



  const [basketQuanitiy, setBasketQuantity] = useState(props.basketProducts.length)
  let endOfTovar;
  if (basketQuanitiy < 2) {
    endOfTovar = ""
  }




    return (
      <div className={classes.modalbasket_main}  style={styleModalContainer}>
        <div className={classes.modalbasket_container} onClick={props.changeModalWindow}>

        </div>
        <div className={classes.modalbasket_window} style={{...styleModalWindow, ...styleModalContainer}}>
          <div className={classes.modalbasket_description_line}>
            {String(basketQuanitiy) + " товар"}
          </div>
          <div className={classes.modalbasket_busketproducts}>
            {props.basketProducts.map((product) => <ProductCard name={product.name} quantity={product.quantity} description={product.description} />)}
          </div>
          <div className={classes.modalbasket_optional_offer}>

          </div>
          <div className={classes.modalbasket_making_offer}>
            <button className={classes.modalbasket_button_offer}>Оформление заказа</button>
          </div>
        </div>
      </div>
    );
}

export default ModalBasket;
