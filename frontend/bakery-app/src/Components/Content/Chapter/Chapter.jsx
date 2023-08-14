import ProductCard from '../ProductCard/ProductCard';
import classes from './Chapter.module.css';



function Chapter(props) {


  let rowLength;
  if (props.windowWidth.isScreenXl) {
    rowLength = 4;
  } else if (props.windowWidth.isScreenLg) {
    rowLength = 3;
  } else if (props.windowWidth.isScreenMd) {
    rowLength = 2;
  }

  const rowsProducts = []

  for (let i = 0; i < props.products.length; i++) {
    const row = [];
    for (let j = 0; j < rowLength; j++) {
      if (typeof props.products[i + j] !== 'undefined') {
        row.push(props.products[i + j])
      }
    }
    rowsProducts.push(row)
    i += rowLength;
  }

  return (
    <div className={classes.chapter_container}>
      <div className={classes.chapter_header}>
        {props.name}
      </div>
      <div className={classes.chapter_products}>
        
          {rowsProducts.map((row, index) =>
          <div className={classes.chapter_products_row} key={index}>
            {row.map(product => <ProductCard product={product} addProduct={props.addProduct} key={product.card_id}/>)}
          </div>
      )}
      
      </div>
    </div>
  );
}

export default Chapter;
