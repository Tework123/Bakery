import classes from './Navbar.module.css';
import axios from 'axios';

function Navbar(props) {

  let style
  // if (props.scroll < 60) {
  //   style = {position: 'static'}
  // } else {
  //   style = {position: 'fixed'}
  // }

  const onClickProfileTest = () => {
    axios.get('/profile').then((response) => {
      console.log(response.data);
    })   
  }
  return (
    <nav className={classes.navbar_container} style={style}>
       <div className={classes.item} onClick={onClickProfileTest}>
              Личный кабинет
            </div>
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
      <div className={classes.item + " " + classes.navbar_basket_button}>
        <button onClick={props.changeModalWindow}>Корзина</button>
      </div>
    </nav>
  );
}

export default Navbar;
