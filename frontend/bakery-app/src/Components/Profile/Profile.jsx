import classes from './Profile.module.css';


function Profile(props) {

  return (
    <div className={classes.profile_container}>
      <div className={classes.profile_user_information}>
        <div className={classes.profile_field_item}>
          <div className={classes.profile_field_text}>Имя</div>
          <input />
        </div>
      </div>
      <div className={classes.profile_order_history}>

      </div>
    </div>
  );
}

export default Profile;
