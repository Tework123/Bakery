import axios from 'axios';
import OrderCard from '../OrderCard/OrderCard';
import classes from './UserOrders.module.css';
import { useEffect, useState } from 'react';

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

  const [userOrders, setUserOrders] = useState([]);

  useEffect(() => {
    axios.get('/profile/orders').then((responce)=> {
      setUserOrders(responce.data)
    })
      axios.get('/main/').then((responce) => {
        console.log(responce.data);
      })
  }, [])

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
        {userOrders.map(order => 
          <OrderCard order={order}/>
        )}
      </div>
    </div>
  );
}

export default UserOrders;
