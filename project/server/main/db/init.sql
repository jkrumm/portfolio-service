drop table if exists binance_orders;

CREATE TABLE binance_orders
(
    id                SMALLINT       NOT NULL AUTO_INCREMENT,
    `timestamp`       DATETIME       NOT NULL,
    symbol            VARCHAR(13)    NOT NULL,
    side              VARCHAR(10)    NOT NULL,
    amount            DECIMAL(25, 6) NOT NULL,
    price             DECIMAL(25, 6) NOT NULL,
    market            DECIMAL(25, 6) NOT NULL,
    market_percentage DECIMAL(7, 2)  NOT NULL,
    PRIMARY KEY (id)
);


# drop table if exists portfolio;

CREATE TABLE portfolio
(
    id                               MEDIUMINT      NOT NULL AUTO_INCREMENT,
    `timestamp`                      DATETIME       NOT NULL,
    btc_usd                          DECIMAL(20, 2) NOT NULL,
    eth_usd                          DECIMAL(20, 2) NOT NULL,
    `current`                        DECIMAL(20, 2) NOT NULL,
    current_btc                      DECIMAL(14, 6) NOT NULL,
    current_24h                      DECIMAL(7, 2),
    current_1w                       DECIMAL(7, 2),
    current_btc_24h                  DECIMAL(7, 2),
    current_btc_1w                   DECIMAL(7, 2),
    current_percentage               DECIMAL(7, 2)  NOT NULL,
    total                            DECIMAL(20, 2) NOT NULL,
    total_btc                        DECIMAL(14, 6) NOT NULL,
    total_24h                        DECIMAL(7, 2),
    total_1w                         DECIMAL(7, 2),
    total_btc_24h                    DECIMAL(7, 2),
    total_btc_1w                     DECIMAL(7, 2),
    binance_total                    DECIMAL(20, 2) NOT NULL,
    binance_total_btc                DECIMAL(14, 6) NOT NULL,
    binance_total_24h                DECIMAL(7, 2),
    binance_total_1w                 DECIMAL(7, 2),
    binance_count                    SMALLINT,
    bitmex_total                     DECIMAL(20, 2) NOT NULL,
    bitmex_total_btc                 DECIMAL(14, 6) NOT NULL,
    bitmex_total_24h                 DECIMAL(7, 2),
    bitmex_total_1w                  DECIMAL(7, 2),
    bitmex_margin                    DOUBLE(20, 2)  NOT NULL,
    bitmex_margin_24h                DECIMAL(7, 2),
    bitmex_margin_1w                 DECIMAL(7, 2),
    bitmex_margin_btc                DECIMAL(14, 6) NOT NULL,
    bitmex_margin_percent            DECIMAL(7, 2)  NOT NULL,
    bitmex_margin_leverage           DECIMAL(20, 2) NOT NULL,
    bitmex_available_margin          DECIMAL(20, 2) NOT NULL,
    bitmex_available_margin_btc      DECIMAL(14, 6) NOT NULL,
    bitmex_unrealised                DECIMAL(20, 2),
    bitmex_unrealised_24h            DECIMAL(7, 2),
    bitmex_unrealised_1w             DECIMAL(7, 2),
    bitmex_unrealised_btc            DECIMAL(14, 6),
    bitmex_unrealised_percentage     DECIMAL(7, 2),
    bitmex_withdraw                  DECIMAL(20, 2),
    bitmex_withdraw_btc              DECIMAL(14, 6),
    bitmex_btc_position              DOUBLE(20, 2),
    bitmex_btc_position_btc          DECIMAL(14, 6),
    bitmex_btc_position_24h          DECIMAL(7, 2),
    bitmex_btc_position_percentage   DECIMAL(7, 2),
    bitmex_btc_position_type         ENUM ('LONG','SHORT'),
    bitmex_btc_position_leverage     DOUBLE(4, 2),
    bitmex_btc_position_opening      DECIMAL(20, 2),
    bitmex_btc_position_opening_date DATETIME,
    bitmex_eth_position              DECIMAL(20, 2),
    bitmex_eth_position_btc          DECIMAL(14, 6),
    bitmex_eth_position_24h          DECIMAL(7, 2),
    bitmex_eth_position_percentage   DECIMAL(7, 2),
    bitmex_eth_position_type         ENUM ('LONG','SHORT'),
    bitmex_eth_position_leverage     DECIMAL(4, 2),
    bitmex_eth_position_opening      DECIMAL(20, 2),
    bitmex_eth_position_opening_date DATETIME,
    atari_total                      DECIMAL(8, 2)  NOT NULL,
    atari_total_btc                  DECIMAL(8, 6)  NOT NULL,
    atari_usd                        DECIMAL(6, 2)  NOT NULL,
    atari_rank                       SMALLINT       NOT NULL,
    atari_rank_delta                 SMALLINT       NOT NULL,
    atari_1d                         DECIMAL(7, 2)  NOT NULL,
    atari_1d_volume                  DECIMAL(7, 2)  NOT NULL,
    atari_7d                         DECIMAL(7, 2)  NOT NULL,
    atari_7d_volume                  DECIMAL(7, 2)  NOT NULL,
    atari_30d                        DECIMAL(7, 2)  NOT NULL,
    atari_30d_volume                 DECIMAL(7, 2)  NOT NULL,
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX portfolio_ix_id ON portfolio (id);


drop table if exists test;

create table test
(
    id  int auto_increment
        primary key,
    val varchar(100) null
);

drop table if exists binance_orders;

CREATE TABLE binance_orders
(
    id                SMALLINT       NOT NULL AUTO_INCREMENT,
    `timestamp`       DATETIME       NOT NULL,
    symbol            VARCHAR(13)    NOT NULL,
    side              VARCHAR(10)    NOT NULL,
    amount            DECIMAL(25, 6) NOT NULL,
    price             DECIMAL(25, 6) NOT NULL,
    market            DECIMAL(25, 6) NOT NULL,
    market_percentage DECIMAL(7, 2)  NOT NULL,
    PRIMARY KEY (id)
);

drop table if exists binance_balances;

CREATE TABLE binance_balances
(
    id              SMALLINT       NOT NULL AUTO_INCREMENT,
    `timestamp`     DATETIME       NOT NULL,
    currency        VARCHAR(6)     NOT NULL,
    amount          DECIMAL(25, 6) NOT NULL,
    price           DECIMAL(20, 2) NOT NULL,
    price_btc       DECIMAL(14, 6),
    balance         DECIMAL(20, 2) NOT NULL,
    balance_btc     DECIMAL(14, 6) NOT NULL,
    used            DECIMAL(25, 6) NOT NULL,
    free            DECIMAL(25, 6) NOT NULL,
    used_percentage DECIMAL(7, 2)  NOT NULL,
    PRIMARY KEY (id)
);


# INSERT INTO portfolio (timestamp, btc_usd, eth_usd, current, current_btc, current_24h, current_1w, current_btc_24h,
#                        current_btc_1w, current_percentage, total, total_btc, total_24h, total_1w, total_btc_24h,
#                        total_btc_1w, binance_total, binance_total_btc, binance_total_24h, binance_total_1w,
#                        binance_count, bitmex_total, bitmex_total_btc, bitmex_total_24h, bitmex_total_1w,
#                        bitmex_margin, bitmex_margin_24h, bitmex_margin_1w, bitmex_margin_btc, bitmex_margin_percent,
#                        bitmex_margin_leverage, bitmex_available_margin, bitmex_available_margin_btc,
#                        bitmex_unrealised, bitmex_unrealised_24h, bitmex_unrealised_1w, bitmex_unrealised_btc,
#                        bitmex_unrealised_percentage, bitmex_withdraw, bitmex_withdraw_btc, bitmex_btc_position,
#                        bitmex_btc_position_btc, bitmex_btc_position_24h, bitmex_btc_position_percentage,
#                        bitmex_btc_position_type, bitmex_btc_position_leverage, bitmex_btc_position_opening,
#                        bitmex_btc_position_opening_date, bitmex_eth_position, bitmex_eth_position_btc,
#                        bitmex_eth_position_24h, bitmex_eth_position_percentage, bitmex_eth_position_type,
#                        bitmex_eth_position_leverage, bitmex_eth_position_opening, bitmex_eth_position_opening_date)
# VALUES ('2021-10-23 12:00:00', 61523.00, 4036.78, 12006.74, 0.195159, 0.05, 0.05, 0.01, 0.01, 26.87, 9463.99, 0.153829,
#         -0.05, -0.05, -0.09, -0.09, 3582.45, 0.058230, 0.02, 0.02, 10, 5881.54, 0.095599, -0.10, -0.10, 8424.34, 0.06,
#         0.06, 0.136930, 76.00, 1.32, 593.88, 0.009653, 2542.75, 0.41, 0.41, 0.041330, 43.23, 2542.75, 0.009653, 1168.08,
#         0.018986, 0.09, 44.00, 'LONG', 2, 34460.92, '2021-07-07 04:00:00', 1373.93, 0.022332, 0.64, 49.00, 'LONG', 2.00,
#         2294.22, '2021-07-29 12:00:00');

drop table if exists marketcap;

CREATE TABLE marketcap
(
    id                    SMALLINT       NOT NULL AUTO_INCREMENT,
    `timestamp`           DATETIME       NOT NULL,
    symbol                VARCHAR(13)    NOT NULL,
    `name`                VARCHAR(40)    NOT NULL,
    price                 DECIMAL(20, 2) NOT NULL,
    marketcap             BIGINT         NOT NULL,
    marketcap_dominance   DECIMAL(7, 2),
    rank_delta            SMALLINT,
    high                  DECIMAL(20, 2),
    high_percentage       DECIMAL(7, 2),
    high_timestamp        TIMESTAMP,
    1d_price_change       DECIMAL(20, 2),
    1d_price_change_pct   DECIMAL(7, 2),
    1d_volume             MEDIUMINT,
    1d_volume_change_pct  DECIMAL(7, 2),
    7d_price_change       DECIMAL(20, 2),
    7d_price_change_pct   DECIMAL(7, 2),
    7d_volume             BIGINT,
    7d_volume_change_pct  DECIMAL(7, 2),
    30d_price_change      DECIMAL(20, 2),
    30d_price_change_pct  DECIMAL(7, 2),
    30d_volume            BIGINT,
    30d_volume_change_pct DECIMAL(7, 2),
    sparkline             JSON,
    PRIMARY KEY (id)
);


drop table if exists job;

CREATE TABLE job
(
    id          BIGINT      NOT NULL AUTO_INCREMENT,
    `timestamp` DATETIME    NOT NULL,
    job         VARCHAR(15) NOT NULL,
    success     BOOLEAN     NOT NULL,
    duration    TIME(3)     NOT NULL,
    `error`     VARCHAR(150),
    PRIMARY KEY (id)
);


drop table if exists worker;

CREATE TABLE worker
(
    id           SMALLINT    NOT NULL AUTO_INCREMENT,
    `timestamp`  DATETIME    NOT NULL,
    lifetime     VARCHAR(20) NOT NULL,
    working_time VARCHAR(20) NOT NULL,
    successful   MEDIUMINT   NOT NULL,
    failed       MEDIUMINT   NOT NULL,
    PRIMARY KEY (id)
);

# drop table if exists pnl;

CREATE TABLE pnl
(
    id                MEDIUMINT      NOT NULL AUTO_INCREMENT,
    `timestamp`       DATETIME       NOT NULL,
    `current`         DECIMAL(20, 2) NOT NULL,
    current_btc       DECIMAL(14, 6) NOT NULL,
    current_24h       DECIMAL(7, 2),
    current_btc_24h   DECIMAL(7, 2),
    binance_total     DECIMAL(20, 2) NOT NULL,
    binance_total_btc DECIMAL(14, 6) NOT NULL,
    binance_total_24h DECIMAL(7, 2),
    bitmex_total      DECIMAL(20, 2) NOT NULL,
    bitmex_total_btc  DECIMAL(14, 6) NOT NULL,
    bitmex_total_24h  DECIMAL(7, 2),
    pnl               DECIMAL(10, 2),
    pnl_binance       DECIMAL(10, 2),
    pnl_bitmex        DECIMAL(10, 2),
    pnl_cum           DECIMAL(7, 2),
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX pnl_ix_id ON pnl (id);

drop table if exists cbbi;

CREATE TABLE cbbi
(
    id          MEDIUMINT NOT NULL AUTO_INCREMENT,
    `timestamp` DATE,
    price       DECIMAL(20, 2),
    confidence  DECIMAL(5, 2),
    puell       DECIMAL(5, 2),
    mvrv        DECIMAL(5, 2),
    rhodl       DECIMAL(5, 2),
    PRIMARY KEY (id)
);
CREATE UNIQUE INDEX cbbi_ix_id ON cbbi (id);

drop table if exists fng;

CREATE TABLE fng
(
    id                   MEDIUMINT NOT NULL AUTO_INCREMENT,
    `timestamp`          DATE,
    `value`              SMALLINT,
    value_classification VARCHAR(50),
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX fng_ix_id ON fng (id);

