import Carusel from './Carusel2/Carusel';
import classes from './CaruselBox.module.css';

function CaruselBox() {
  return (
    <div className={classes.carusel_container}>
      <Carusel/>
    </div>
  );
}

export default CaruselBox;
