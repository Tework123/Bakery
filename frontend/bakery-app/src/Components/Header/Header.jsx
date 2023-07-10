import classes from './Header.module.css';

function Header() {
  return (
    <header className={classes.header_container}>
      <div className={classes.header_main}>
        <div>Logo</div>
        <div>Телефон, адрес</div>
        <div className={classes.right_actions}>
          <div className={classes.item}>
            Вход
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
