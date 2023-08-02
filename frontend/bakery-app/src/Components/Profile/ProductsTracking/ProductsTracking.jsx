import { useEffect, useState } from 'react';
import classes from './ProductsTracking.module.css';
import axios from 'axios';

function ProductsTracking(props) {

  useEffect(() => {
    /*axios.get('/restaurant/cards').then((responce) => {
      console.log(responce.data);
    })*/
  }, [])
  


  return (
    <div className={classes.producttr_container}>
      <header className={classes.title}>Продукты</header>
      <button className={classes.producttr_button_add_product}>Добавить товар</button>
      <div className={classes.producttr_search}>
        Search_лупа
      </div>
      <table className={classes.producttr_table}>
        <tr>
          <th>Название</th>
          <th>Категория</th>
          <th>ID</th>
        </tr>
        <tr>
          <td>Осетинский пирог</td>
          <td>Пироги</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Булочка с корицей</td>
          <td>Булочки</td>
          <td>2</td>
        </tr>
        <tr>
          <td>Булочка с маслом</td>
          <td>Булочки</td>
          <td>3</td>
        </tr>
        <tr>
          <td>Булочка с вишней</td>
          <td>Булочки</td>
          <td>4</td>
        </tr>
        <tr>
          <td>Комбо 2 в одном</td>
          <td>Комбо</td>
          <td>5</td>
        </tr>
        <tr>
          <td>Молочный коктейль</td>
          <td>Напитки</td>
          <td>6</td>
        </tr>
      </table>
    </div>
  );
}

export default ProductsTracking;
