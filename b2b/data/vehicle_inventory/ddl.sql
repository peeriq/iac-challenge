CREATE DATABASE vehicle_inventory;

CREATE TABLE IF NOT EXISTS vehicles (
  id bigint GENERATED ALWAYS AS IDENTITY (CACHE 200) PRIMARY KEY,
  vin varchar(20) UNIQUE,
  year smallint NOT NULL,
  model varchar(50) NOT NULL ,
  make varchar(50) NOT NULL,
  price numeric(9,2) NOT NULL,
  country varchar(50) NOT NULL,
  postal_code varchar(50),
  state varchar(50),
  city varchar(50) NOT NULL,
  street_address varchar(50) NOT NULL
);