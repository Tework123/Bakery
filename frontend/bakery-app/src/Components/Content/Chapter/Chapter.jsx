import ProductCard from '../ProductCard/ProductCard';
import classes from './Chapter.module.css';



function Chapter({name, products, addProduct}) {



  //функция в зависимости от количества текста будет менять
  //высоту карточки, а также добавлять пустые карточки, чтобы 
  //всё было в ряд ровно
  function productsInChapter() {

  }

  return (
    <div className={classes.chapter_container}>
      <div className={classes.chapter_header}>
        {name}
      </div>
      <div className={classes.chapter_products}>
        
          {products.map((product) =>
              <ProductCard name={product.name} price={product.price} imageURL={product.image} description={product.description} id={product.card_id} addProduct={addProduct}/>
            )}
      
      </div>
    </div>
  );
}

export default Chapter;
