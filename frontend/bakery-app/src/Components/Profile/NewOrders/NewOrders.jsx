import { useEffect, useState } from 'react';
import classes from './NewOrders.module.css';
import axios from 'axios';

function NewOrders(props) {

  const [orders, setOrders] = useState([])
  const [selected, setSelected] = useState(null)

  const onClickOrder = (id) => {
    const newArrayOrders = [...orders]
    newArrayOrders.forEach(order => {
      debugger
      if (order.order_id === id) {
        order.selected = true;
        setSelected(id)
      } else {
        order.selected = false;
      }
    });
    setOrders(newArrayOrders);
    console.log(newArrayOrders);
  }


  useEffect(() => {
    axios.get('/restaurant/current_orders').then((responce) => {
      setOrders(responce.data.map(order => ({...order, selected: false})))
    })
  }, [])

  return (
    <div className={classes.neworder_container}>
      <div className={classes.fixed_actions_container}>
        <div>
          
        </div>
      </div>
      <header className={classes.title}>Текущие заказы</header>
      {orders.map(order =>
        <div className={order.selected ? classes.neworder_item + ' ' + classes.selected : classes.neworder_item} onClick={e => onClickOrder(order.order_id)}>
          <div className={classes.neworder_information}>
            <div className={classes.neworder_name_id}>
              Заказ №{order.order_id}
            </div>
            <div className={classes.neworder_date}>
              {order.date}
            </div>
            <div className={classes.neworder_address}>
              {`Адрес: ${order.address}`}
            </div>
          </div>
          <div className={classes.neworder_products}>
          <header className={classes.neworder_title}>Товары</header>
          <table>
            <tbody>
              {order.cards.map(product => (
                <tr>
                  <td>{product.name}</td>
                  <td>x{product.amount}</td>
                </tr>
              ))}
            </tbody>
          </table>
          </div>
        </div>
      )}

    </div>
  );
}

export default NewOrders;
