import { NavLink } from 'react-router-dom';
import classes from './NavbarEmployeeProfile.module.css';


function NavbarEmployeeProfile(props) {


  return (
    <nav className={classes.navbaremp_container}>
      <NavLink
        to='/profile'
        className={classes.navbaremp_item}>    
        Личная информация

      </NavLink>
      <NavLink
        to='orders'
        className={classes.navbaremp_item}>

        Заказы

      </NavLink>
      <NavLink
        to='products'
        className={classes.navbaremp_item}>

        Продукты

      </NavLink>
    </nav>
  );
}

export default NavbarEmployeeProfile;
