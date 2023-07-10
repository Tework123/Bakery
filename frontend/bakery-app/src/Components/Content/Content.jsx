import Chapter from './Chapter/Chapter';
import classes from './Content.module.css';

function Content(props) {

  const test_data_chapters = [
    {
      name: 'Выпечка'
    },
    {
      name: 'Хлебушек'
    },
    {
      name: 'Пироги'
    },
    {
      name: 'Десерты'
    }
  ]

  return (
    <div className={classes.content_container}>
      <header className={classes.content_header}>
        <span className={classes.content_header_text}>
          Наши товары
        </span>
      </header >
      <div className={classes.content_catalog}>
        {test_data_chapters.map((chapter) => 
          <Chapter products={props.products} name={chapter.name}/>
        )}
      </div>
    </div>
  );
}

export default Content;
