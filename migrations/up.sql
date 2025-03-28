CREATE TABLE IF NOT EXISTS users (
  id integer PRIMARY KEY,
  name varchar(20) NOT NULL,
  mean_rating float
);

CREATE TABLE IF NOT EXISTS usersLogin (
  id integer PRIMARY KEY REFERENCES users (id),
  email varchar(254) UNIQUE,
  hash varchar(60),
  deliveryAddr text,
  CONSTRAINT
    proper_email CHECK (email ~* '^[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$')
);

CREATE TABLE IF NOT EXISTS salts (
  id integer PRIMARY KEY REFERENCES users (id),
  salt varchar(20),
)

CREATE TABLE IF NOT EXISTS items (
  item_id integer PRIMARY KEY,
  seller_id integer REFERENCES users (id)
  name varchar(50) NOT NULL,
  description varchar(300) NOT NULL,
  price_pennies integer CHECK (price_pennies > 0) NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
  transaction_id integer PRIMARY KEY,
  seller_id integer REFERENCES users (id),
  buyer_id integer REFERENCES users (id) CHECK (seller_id != buyer_id),
);

CREATE TABLE IF NOT EXISTS reviews (
  seller_id integer REFERENCES users (id)
  buyer_id integer REFERENCES users (id) CHECK (seller_id != buyer_id),
  rating integer CHECK (rating <= 5),
);
