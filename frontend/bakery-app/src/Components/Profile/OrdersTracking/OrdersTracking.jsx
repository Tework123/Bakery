import OrdersFindForm from './OrdersFindForm/OrdersFindForm';
import classes from './OrdersTracking.module.css';

function OrdersTracking(props) {
  
  
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
