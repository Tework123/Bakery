import classes from './ProductAddChange.module.css';

function ProductAddChange(props) {
  
  
  return (
    <div className={classes.productchange_container}>
      <div>
        <div>Название</div>
        <input></input>
      </div>
      <div>
        <div>Словесное описание</div>
        <input></input>
      </div>
      
    </div>
  );
}

export default ProductAddChange;
