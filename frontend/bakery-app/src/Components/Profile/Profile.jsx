import React, { useEffect, useState } from 'react';
import classes from './Profile.module.css';
import axios from 'axios';
import NavbarEmployeeProfile from './NavbarEmployeeProfile/NavbarEmployeeProfile';
import { Route, Routes, useNavigate } from 'react-router-dom';
import OrdersTracking from './OrdersTracking/OrdersTracking';
import ProductsTracking from './ProductsTracking/ProductsTracking';


function Profile(props) {
  


  useEffect(() => {
    // axios.get('/restaurant/cards').then((responce) => {
    //   setTestImage(URL.createObjectURL(responce.data))
    // })
  }, [])

  const profileAccoutInfo = (
    <React.Fragment>
      <div className={classes.profile_user_information}>
        <header className={classes.title}>Личная информация</header>
        <div className={classes.profile_field_item}>
          <div className={classes.profile_field_text}>Имя</div>
          <input />
        </div>
      </div>
      <div className={classes.profile_order_history}>

      </div>
    </React.Fragment>
  )

  return (
    <div className={classes.profile_container}>
      <NavbarEmployeeProfile/>
      <Routes>
        <Route
          path='orders'
          element={<OrdersTracking/>}/>
        <Route
          path='products'
          element={<ProductsTracking/>}/>
        <Route
          path='/'
          element={profileAccoutInfo}/>
      </Routes>
     
        
      </div>
  );
}

export default Profile;
