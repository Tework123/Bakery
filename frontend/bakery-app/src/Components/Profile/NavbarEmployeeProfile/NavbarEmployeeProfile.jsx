import { NavLink } from 'react-router-dom';
import classes from './NavbarEmployeeProfile.module.css';
import React from 'react';


function NavbarEmployeeProfile(props) {


  return (
    <nav className={classes.navbaremp_container}>
      <NavLink
        to='information'
        className={({isActive, isPending}) =>
          isPending ? classes.isPending + " " + classes.navbaremp_item : isActive ? classes.isActive + " " + classes.navbaremp_item: classes.isPending + " " + classes.navbaremp_item}>    
        Данные аккаунта

      </NavLink>
      <NavLink
        to='orders'
        className={({isActive, isPending}) =>
          isPending ? classes.isPending + " " + classes.navbaremp_item: isActive ? classes.isActive + " " + classes.navbaremp_item: classes.isPending + " " + classes.navbaremp_item}>

        Заказы

      </NavLink>
      <NavLink
        to='products'
        className={({isActive, isPending}) =>
          isPending ? classes.isPending + " " + classes.navbaremp_item: isActive ? classes.isActive + " " + classes.navbaremp_item: classes.isPending + " " + classes.navbaremp_item}>


        Товары

      </NavLink>
      
      {props.userType === 'main_admin' ? <React.Fragment>
      <NavLink
        to='workers'
        className={({isActive, isPending}) =>
          isPending ? classes.isPending + " " + classes.navbaremp_item: isActive ? classes.isActive + " " + classes.navbaremp_item: classes.isPending + " " + classes.navbaremp_item}>


        Сотрудники

      </NavLink>
      <NavLink
        to='sitedata'
        className={({isActive, isPending}) =>
          isPending ? classes.isPending + " " + classes.navbaremp_item: isActive ? classes.isActive + " " + classes.navbaremp_item: classes.isPending + " " + classes.navbaremp_item}>


        Данные сайта

      </NavLink>
      </React.Fragment> : ''}
    </nav>
  );
}

export default NavbarEmployeeProfile;
