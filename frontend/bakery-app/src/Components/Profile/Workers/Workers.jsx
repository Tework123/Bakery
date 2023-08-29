import Worker from './Worker/Worker';
import classes from './Workers.module.css';

function Workers(props) {
  
  const workers = [
    {
      name: 'Паша',
      image: null
    },
    {
      name: 'Евгений Пирожков Александрович',
      image: null
    },
    {
      name: 'Евгений Пирожков Александрович',
      image: null
    },
    {
      name: 'Евгений Пирожков Александрович',
      image: null
    },
    {
      name: 'Евгений Пирожков Александрович',
      image: null
    },
    {
      name: 'Евгений Пирожков Александрович',
      image: null
    },
    {
      name: 'Евгений Пирожков Александрович',
      image: null
    },
    {
      name: 'Евгений Пирожков Александрович',
      image: null
    },
    {
      name: 'Евгений Пирожков Александрович',
      image: null
    },
  ]

  return (
    <div className={classes.workers_container}>
      <header className={classes.title}>Работники</header>
      <button className={classes.add_worker_button}>Добавить работника</button>
      <div className={classes.workers_list}>
        {workers.map(worker => <Worker image={worker.image} name={worker.name}/>)}
      </div>
    </div>
  );
}

export default Workers;
