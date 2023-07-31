import React, { useState, useRef, useEffect } from 'react';
import classes from './ModalBasket.module.css';
import ProductCard from './ProductCard/ProductCard';
import axios from 'axios';

function ModalBasket(props) {


  let ref = useRef(null)

  const onScrollContainer = (e) => {
    ref.current.scrollTop =ref.current.scrollTop + e.deltaY
  }

  let styleModalContainer;
  let styleModalWindow;

  if (props.isModalBasketOpen) {
    styleModalContainer = { display: 'flex' }
    styleModalWindow = {right: 0}
  } else {
    styleModalContainer = { display: 'none' }
    styleModalWindow = {right: 450}
  }

    return (
      <div className={classes.modalbasket_main} style={styleModalContainer} onWheel={(e) => { onScrollContainer(e) }}>
        <div className={classes.modalbasket_container} onClick={props.changeModalWindow} >

        </div>
        <div ref={ref} className={classes.modalbasket_window} style={{ ...styleModalWindow, ...styleModalContainer }}>
          {!props.isAuthorizated ? undefined :
            <React.Fragment>
              <div className={classes.modalbasket_description_line}>
              </div>
              <div className={classes.modalbasket_busketproducts}>
                {props.basketProducts.map((product) => <ProductCard product={product} changeBasket={props.changeBasket} />)}
              </div>
              <div className={classes.modalbasket_optional_offer}>

              </div>
              <div className={classes.modalbasket_making_offer}>
                <button className={classes.modalbasket_button_offer}>Оформление заказа</button>
              </div>
            </React.Fragment>
          }
        </div>
      </div>
    );
}

export default ModalBasket;
