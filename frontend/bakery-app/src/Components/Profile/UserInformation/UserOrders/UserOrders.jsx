import axios from 'axios';
import OrderCard from '../OrderCard/OrderCard';
import classes from './UserOrders.module.css';
import { useState } from 'react';

function UserOrders(props) {


  const active = 'active'
  const completed = 'completed'
  const [ordersType, setOrdersType] = useState(active)

  const onChangeTypeOrders = (type) => {

  }
  const onClickActiveOrders = () => {
    setOrdersType(active)
  }
  const onClickCompletedOrders = () => {
    setOrdersType(completed)
  }

  const getStyle = (type) => {
    if (type === active) {
      if (ordersType === active) {
        return classes.active
      } else {
        return
      }
    } else {
      if (ordersType === completed) {
        return classes.active
      } else {
        return
      } 
    }
  }

  return (
    <div className={classes.userorders_container}>
      <div className={classes.userorders_header}>
        <header className={classes.title}>Мои заказы</header>
        <div className={classes.userorders_header_actions}>
          <button
            onClick={onClickActiveOrders}
            className={classes.left + ' ' + getStyle(active)}>
            Активные
          </button>
          <button
            onClick={onClickCompletedOrders}
            className={classes.right + ' ' + getStyle(completed)}>
            Завершенные
          </button>
        </div>
      </div>
      <div className={classes.userorders_cards}>
        <OrderCard />
        <OrderCard />
        <OrderCard />
      </div>
    </div>
  );
}

export default UserOrders;
