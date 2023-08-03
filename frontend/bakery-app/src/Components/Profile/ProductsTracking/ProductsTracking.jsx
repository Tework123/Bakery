import { useEffect, useState } from 'react';
import classes from './ProductsTracking.module.css';
import axios from 'axios';

function ProductsTracking(props) {

  const [products, setProducts] = useState([
    {
      name: 'Осетинский пирог',
      category: 'Пироги',
      id:1
    },
    {
      name: 'Булочка с корицей',
      category: 'Булочки',
      id:2
    },
    {
      name: 'Булочка с маслом',
      category: 'Булочки',
      id:3
    },
    {
      name: 'Комбо 2 в одном',
      category: 'Комбо',
      id:4
    },
  ])

  useEffect(() => {
    /*axios.get('/restaurant/cards').then((responce) => {
      console.log(responce.data);
    })*/
  }, [])

  const openProductEditor = (id) => {
    window.open(`editor/${id}`)
  }


  return (
    <div className={classes.producttr_container}>
      <header className={classes.title}>Продукты</header>
      <div className={classes.producttr_uptable_actions}>
        <div className={classes.producttr_search}>
          <input></input>
        </div>
        <button className={classes.producttr_button_add_product}>Добавить товар</button>
      </div>
      <table className={classes.producttr_table}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Категория</th>
          </tr>
        </thead>
        <tbody>
          {products.map(product => (
            <tr onClick={e => openProductEditor(product.id)}>
              <td>{product.id}</td>
              <td>{product.name}</td>
              <td>{product.category}</td>
            </tr>))}
        </tbody>
      </table>
    </div>
  );
}

export default ProductsTracking;
