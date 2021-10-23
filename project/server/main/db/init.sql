drop table if exists binance_orders;

CREATE TABLE binance_orders(
                               id SMALLINT NOT NULL AUTO_INCREMENT,
                               `timestamp` DATETIME NOT NULL,
                               symbol VARCHAR(13) NOT NULL,
                               side VARCHAR(10) NOT NULL,
                               amount DECIMAL(25,6) NOT NULL,
                               price DECIMAL(25,6) NOT NULL,
                               market DECIMAL(25,6) NOT NULL,
                               market_percentage DECIMAL(7,2) NOT NULL,
                               PRIMARY KEY(id)
);

drop table if exists binance_balances;

CREATE TABLE binance_balances(
                                 id SMALLINT NOT NULL AUTO_INCREMENT,
                                 timstamp DATETIME NOT NULL,
                                 currency VARCHAR(6) NOT NULL,
                                 amount DECIMAL(25,6) NOT NULL,
                                 price DECIMAL(20,2) NOT NULL,
                                 price_btc DECIMAL(14,6) NOT NULL,
                                 balance DECIMAL(20,2) NOT NULL,
                                 balance_btc DECIMAL(14,6) NOT NULL,
                                 used DECIMAL(25,6) NOT NULL,
                                 free DECIMAL(25,6) NOT NULL,
                                 used_percentage DECIMAL(7,2) NOT NULL,
                                 PRIMARY KEY(id)
);

--drop table if exists portfolio;

CREATE TABLE portfolio(
                          id MEDIUMINT NOT NULL AUTO_INCREMENT,
                          `timestamp` DATETIME NOT NULL,
                          btc_usd DECIMAL(20,2) NOT NULL,
                          eth_usd DECIMAL(20,2) NOT NULL,
                          `current` DECIMAL(20,2) NOT NULL,
                          current_btc DECIMAL(14,6) NOT NULL,
                          current_24h DECIMAL(7,2),
                          current_1w DECIMAL(7,2),
                          current_btc_24h DECIMAL(7,2),
                          current_btc_1w DECIMAL(7,2),
                          current_percentage DECIMAL(7,2) NOT NULL,
                          total DECIMAL(20,2) NOT NULL,
                          total_btc DECIMAL(14,6) NOT NULL,
                          total_24h DECIMAL(7,2),
                          total_1w DECIMAL(7,2),
                          total_btc_24h DECIMAL(7,2),
                          total_btc_1w DECIMAL(7,2),
                          binance_total DECIMAL(20,2) NOT NULL,
                          binance_total_btc DECIMAL(14,6) NOT NULL,
                          binance_total_24h DECIMAL(7,2),
                          binance_total_1w DECIMAL(7,2),
                          binance_count INT,
                          bitmex_total DECIMAL(20,2) NOT NULL,
                          bitmex_total_btc DECIMAL(14,6) NOT NULL,
                          bitmex_total_24h DECIMAL(7,2),
                          bitmex_total_1w DECIMAL(7,2),
                          bitmex_margin DOUBLE(20,2) NOT NULL,
                          bitmex_margin_24h DECIMAL(7,2),
                          bitmex_margin_1w DECIMAL(7,2),
                          bitmex_margin_btc DECIMAL(14,6) NOT NULL,
                          bitmex_margin_percent DECIMAL(7,2) NOT NULL,
                          bitmex_margin_leverage DECIMAL(20,2) NOT NULL,
                          bitmex_available_margin DECIMAL(20,2) NOT NULL,
                          bitmex_available_margin_btc DECIMAL(14,6) NOT NULL,
                          bitmex_unrealised DECIMAL(20,2) NOT NULL,
                          bitmex_unrealised_24h DECIMAL(7,2),
                          bitmex_unrealised_1w DECIMAL(7,2),
                          bitmex_unrealised_btc DECIMAL(14,6) NOT NULL,
                          bitmex_unrealised_percentage DECIMAL(7,2) NOT NULL,
                          bitmex_withdraw DECIMAL(20,2) NOT NULL,
                          bitmex_withdraw_btc DECIMAL(14,6) NOT NULL,
                          bitmex_btc_position DOUBLE(20,2) NOT NULL,
                          bitmex_btc_position_btc DECIMAL(14,6) NOT NULL,
                          bitmex_btc_position_24h DECIMAL(7,2),
                          bitmex_btc_position_percentage DECIMAL(7,2) NOT NULL,
                          bitmex_btc_position_type ENUM('LONG','SHORT') NOT NULL,
                          bitmex_btc_position_leverage DOUBLE(4,2) NOT NULL,
                          bitmex_btc_position_opening DECIMAL(20,2) NOT NULL,
                          bitmex_btc_position_opening_date DATETIME NOT NULL,
                          bitmex_eth_position DECIMAL(20,2) NOT NULL,
                          bitmex_eth_position_btc DECIMAL(14,6) NOT NULL,
                          bitmex_eth_position_24h DECIMAL(7,2),
                          bitmex_eth_position_percentage DECIMAL(7,2) NOT NULL,
                          bitmex_eth_position_type ENUM('LONG','SHORT') NOT NULL,
                          bitmex_eth_position_leverage DECIMAL(4,2) NOT NULL,
                          bitmex_eth_position_opening DECIMAL(20,2) NOT NULL,
                          bitmex_eth_position_opening_date DATETIME NOT NULL,
                          PRIMARY KEY(id)
);

CREATE UNIQUE INDEX portfolio_ix_id ON portfolio(id);

