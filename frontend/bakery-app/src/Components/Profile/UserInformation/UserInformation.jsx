import { useNavigate } from 'react-router-dom';
import classes from './UserInformation.module.css';
import UserOrders from './UserOrders/UserOrders';

function UserInformation(props) {
  
  const navigate = useNavigate()

  const exitFromAccount = () => {
    props.authorization.unAuthorize();
    navigate("../../main");
  }

  return (
    <div className={classes.user_information}>
      <div className={classes.profile_user_information}>
        <header className={classes.title}>Личная информация</header>
        <div className={classes.profile_field_item}>
          <div className={classes.profile_field_name}>Почта</div>
          <input />

        </div>
        <div className={classes.action}>
          <button style={{ border: '1px solid black' }} onClick={exitFromAccount}>
            Выйти
          </button>
        </div>
      </div>
      <UserOrders/>
    </div>
  );
}

export default UserInformation;
