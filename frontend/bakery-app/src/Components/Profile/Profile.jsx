import React, { useEffect, useState } from 'react';
import classes from './Profile.module.css';
import axios from 'axios';
import NavbarEmployeeProfile from './NavbarEmployeeProfile/NavbarEmployeeProfile';
import { Route, Routes, useNavigate } from 'react-router-dom';
import OrdersTracking from './OrdersTracking/OrdersTracking';
import ProductsTracking from './ProductsTracking/ProductsTracking';
import Cookies from 'js-cookie'

function Profile(props) {
  
  const navigate = useNavigate()

  const exitFromAccount = () => {
    Cookies.remove('remember_token2')
    props.authorization.unAuthorize()
    navigate("../../main");
  }


  const profileAccoutInfo = (
    <React.Fragment>
      <div className={classes.profile_user_information}>
        <header className={classes.title}>Личная информация</header>
        <div className={classes.profile_field_item}>
          <div className={classes.profile_field_name}>Имя</div>
          <div className={classes.profile_field_input_row}>
            <input />
            <div className={classes.profile_field_name_action_change}>
              Изменить
            </div>
          </div>
        </div>
        <div className={classes.profile_field_item}>
          <div className={classes.profile_field_name}>Почта</div>
          <input />

        </div>
      </div>
      <header className={classes.title}>История заказов</header>
      <div className={classes.profile_order_history}>

      </div>
      <button style={{border: '1px solid black'}} onClick={exitFromAccount}>Выйти</button>
    </React.Fragment>
  )

  return (
    <div className={classes.profile_container}>
      {props.authorization.userType === 'restaurant' || props.authorization.userType === 'main_admin' ? <NavbarEmployeeProfile userType={props.authorization.userType}/> : ''}
      <Routes>
      <Route
          path='information'
          element={profileAccoutInfo} />

        {props.authorization.userType === 'restaurant' || props.authorization.userType === 'main_admin' ? <React.Fragment>
          <Route
            path='orders'
            element={<OrdersTracking />} />
          <Route
            path='products'
            element={<ProductsTracking />} />
        </React.Fragment> : ''}

        {props.authorization.userType === 'main_admin' ? <React.Fragment>
          <Route
            path='workers'
            element={<ProductsTracking />} />
          <Route
            path='sitedata'
            element={<ProductsTracking />} />
        </React.Fragment> : ''}
      </Routes>
     
        
      </div>
  );
}

export default Profile;
