CREATE TABLE IF NOT EXISTS users (
  name varchar(20) PRIMARY KEY,
  email varchar(254) UNIQUE,
  hash varchar(100),
  CONSTRAINT
    proper_email CHECK (email ~* '^[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$')
);

CREATE TABLE IF NOT EXISTS usersShippingAddress (
  name varchar(20) PRIMARY KEY REFERENCES users (name),
  post_code varchar(8) NOT NULL,
  addr_line1 text NOT NULL,
  addr_line2 text,
  addr_level2 text,
  addr_level1 text,
  CONSTRAINT
    proper_post_code CHECK (post_code ~* '^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$')
);

CREATE TABLE IF NOT EXISTS usersRatings (
  name varchar(20) PRIMARY KEY REFERENCES users (name),
  mean_rating float
);

CREATE TABLE IF NOT EXISTS items (
  item_id integer PRIMARY KEY,
  seller_id varchar(20) REFERENCES users (name),
  name varchar(50) NOT NULL,
  description varchar(300) NOT NULL,
  price_pennies integer CHECK (price_pennies > 0) NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
  transaction_id integer PRIMARY KEY,
  seller_id varchar(20) REFERENCES users (name),
  buyer_id varchar(20) REFERENCES users (name) CHECK (seller_id != buyer_id)
);

CREATE TABLE IF NOT EXISTS reviews (
  seller_id varchar(20) REFERENCES users (name),
  buyer_id varchar(20) REFERENCES users (name) CHECK (seller_id != buyer_id),
  rating integer CHECK (rating <= 5)
);
