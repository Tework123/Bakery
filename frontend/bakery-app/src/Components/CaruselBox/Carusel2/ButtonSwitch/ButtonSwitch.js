import classes from './ButtonSwitch.module.css';

function ButtonSwitch(props) {

  return (
    <button className={classes.button} onClick={props.onClick}>+</button>
  );
}

export default ButtonSwitch;
