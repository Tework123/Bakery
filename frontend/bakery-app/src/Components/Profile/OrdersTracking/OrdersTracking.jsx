import { useEffect, useState } from 'react';
import OrdersFindForm from './OrdersFindForm/OrdersFindForm';
import classes from './OrdersTracking.module.css';
import axios from 'axios';

function OrdersTracking(props) {
  
  const [orders, setOrders] = useState([])

  useEffect(() => {
    axios.get('orders/current_orders').then((responce) => {
      setOrders(responce.data)
    })
  })

  return (
    <div className={classes.ordertr_container}>
      <header className={classes.title}>Заказы</header>
      <OrdersFindForm/>
      <table >
        <thead>
        <tr>
          <th>
            ---
          </th>
          <th>
            ID
          </th>
          <th>
            Статус
          </th>
          <th>
            Сообщение
          </th>
          <th>
            Дата
          </th>
          <th>
            Адресс
          </th>
        </tr>
        </thead>
        <tbody>
          {orders.map(order =>
          <tr>
            <th></th>
            <th>{order.order_id}</th>
            <th>{order.status}</th>
            <th>{order.text}</th>
            <th>{order.date}</th>
            <th>{order.address}</th>
          </tr>)}
        </tbody>
      </table>
    </div>
  );
}

export default OrdersTracking;
