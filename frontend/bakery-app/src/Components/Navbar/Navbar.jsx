import classes from './Navbar.module.css';
import axios from 'axios';

function Navbar(props) {


  const onClickProfileTest = () => {
    axios.get('/profile/pass_orders').then((response) => {
      console.log(response.data);
    })   
  }
  return (
    <nav className={classes.navbar_container}>
      <div className={classes.navbar_logo + " " + classes.item}>

      </div>
      <div className={classes.item}>
        Выпечка
      </div>
      <div className={classes.item}>
        Хлебушек
      </div>
      <div className={classes.item}>
        Другие товары
      </div>
      <div className={classes.item}>
        Пироги
      </div>
      <button
        className={classes.item + " " + classes.navbar_basket_button}
        onClick={props.changeModalWindow}>
        Корзина
      </button>
    </nav>
  );
}

export default Navbar;
