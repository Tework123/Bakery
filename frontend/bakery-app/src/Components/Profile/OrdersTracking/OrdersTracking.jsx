import { useEffect } from 'react';
import OrdersFindForm from './OrdersFindForm/OrdersFindForm';
import classes from './OrdersTracking.module.css';
import axios from 'axios';

function OrdersTracking(props) {
  
  
  useEffect(() => {
    axios.get('/restaurant/orders').then((responce) => {
      console.log(responce.data);
    })
  })
  return (
    <div className={classes.ordertr_container}>
      <header className={classes.title}>Заказы</header>
      <OrdersFindForm/>
      <table >
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
        </tr>
      </table>
    </div>
  );
}

export default OrdersTracking;
