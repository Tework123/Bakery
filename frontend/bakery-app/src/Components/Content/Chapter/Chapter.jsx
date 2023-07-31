import ProductCard from '../ProductCard/ProductCard';
import classes from './Chapter.module.css';



function Chapter(props) {



  //функция в зависимости от количества текста будет менять
  //высоту карточки, а также добавлять пустые карточки, чтобы 
  //всё было в ряд ровно
  function productsInChapter() {

  }

  return (
    <div className={classes.chapter_container}>
      <div className={classes.chapter_header}>
        {props.name}
      </div>
      <div className={classes.chapter_products}>
        
          {props.products.map((product) =>
              <ProductCard product={product} addProduct={props.addProduct} key={product.card_id}/>
            )}
      
      </div>
    </div>
  );
}

export default Chapter;
