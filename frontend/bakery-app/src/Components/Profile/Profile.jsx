import React from 'react';
import classes from './Profile.module.css';
import NavbarEmployeeProfile from './NavbarEmployeeProfile/NavbarEmployeeProfile';
import { Route, Routes } from 'react-router-dom';
import OrdersTracking from './OrdersTracking/OrdersTracking';
import ProductsTracking from './ProductsTracking/ProductsTracking';
import UserInformation from './UserInformation/UserInformation';
import Workers from './Workers/Workers';
import ProductEditor from './ProductEditor/ProductEditor';
import NewOrders from './NewOrders/NewOrders';

function Profile(props) {

  

  return (
    <div className={classes.profile_container}>
      {props.authorization.userType === 'restaurant' || props.authorization.userType === 'main_admin' ? <NavbarEmployeeProfile userType={props.authorization.userType}/> : ''}
      <Routes>
      <Route
          path='information'
          element={<UserInformation authorization={props.authorization}/>} />

        {props.authorization.userType === 'restaurant' || props.authorization.userType === 'main_admin' ? <React.Fragment>
          <Route
            path='orders'
            element={<OrdersTracking />} />
          <Route
            path='products'
            element={<ProductsTracking />} />
          <Route
            path='editor/:card_id'
            element={<ProductEditor/>} />
          <Route
            path='neworders'
            element={<NewOrders/>} />
        </React.Fragment> : ''}

        {props.authorization.userType === 'main_admin' ? <React.Fragment>
          <Route
            path='workers'
            element={<Workers />} />
          <Route
            path='sitedata'
            element={<ProductsTracking />} />
        </React.Fragment> : ''}
      </Routes>
     
        
      </div>
  );
}

export default Profile;
