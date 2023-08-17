import classes from './OrdersFindForm.module.css';

function OrdersFindForm(props) {
  
  
  return (
    <form className={classes.findform}>
      <div className={classes.inputs}>
        <div className={classes.input_item}>
          <div className={classes.name}>
            ID
          </div>
          <div>
            <input></input>
            <span>- - -</span>
            <input></input>
          </div>
        </div>
        <div className={classes.input_item}>
          <div className={classes.name}>
            Статус
          </div>
          <div className={classes.list}>
            <select>
              <option>  Все        </option>
              <option>  Доставлен </option>
              <option>  В процессе</option>
            </select>
          </div>
        </div>
        <div className={classes.input_item}>
          <div className={classes.name}>
            Дата
          </div>
          <div>
            <input type='date' ></input>
            <span>- - -</span>
            <input type='date' ></input>
          </div>
        </div>
      </div>
      <div className={classes.actions}>
        <button>Найти</button>
        <button>Сбросить</button>
      </div>
    </form>
  );
}

export default OrdersFindForm;
