import classes from './Worker.module.css';

function Worker(props) {
  
  return (
    <div className={classes.worker_container}>
      <div className={classes.image}>
        <img alt='No image' src={props.image} loading="lazy"/>
      </div>
      <div className={classes.name}>
        {props.name}
      </div>
    </div>
  );
}

export default Worker;
