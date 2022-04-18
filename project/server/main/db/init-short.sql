create table if not exists binance_balances
(
    id              smallint auto_increment
        primary key,
    timestamp       datetime       not null,
    currency        varchar(6)     not null,
    amount          decimal(25, 6) not null,
    price           decimal(20, 2) not null,
    price_btc       decimal(14, 6) null,
    balance         decimal(20, 2) not null,
    balance_btc     decimal(14, 6) not null,
    used            decimal(25, 6) not null,
    free            decimal(25, 6) not null,
    used_percentage decimal(7, 2)  not null
);

create table if not exists binance_orders
(
    id                smallint auto_increment
        primary key,
    timestamp         datetime       not null,
    symbol            varchar(13)    not null,
    side              varchar(10)    not null,
    amount            decimal(25, 6) not null,
    price             decimal(25, 6) not null,
    market            decimal(25, 6) not null,
    market_percentage decimal(7, 2)  not null
);

create table if not exists cbbi
(
    id         mediumint auto_increment
        primary key,
    timestamp  date           null,
    price      decimal(20, 2) null,
    confidence decimal(5, 2)  null,
    puell      decimal(5, 2)  null,
    mvrv       decimal(5, 2)  null,
    rhodl      decimal(5, 2)  null,
    constraint cbbi_ix_id
        unique (id)
);

create table if not exists fng
(
    id                   mediumint auto_increment
        primary key,
    timestamp            date        null,
    value                smallint    null,
    value_classification varchar(50) null,
    constraint fng_ix_id
        unique (id)
);

create table if not exists global
(
    id                     bigint auto_increment
        primary key,
    timestamp              datetime      not null,
    btc_dominance          decimal(4, 2) not null,
    eth_dominance          decimal(4, 2) not null,
    total_market_cap       bigint        not null,
    total_volume_24h       bigint        not null,
    altcoin_volume_24h     bigint        not null,
    altcoin_market_cap     bigint        not null,
    defi_volume_24h        bigint        not null,
    defi_market_cap        bigint        not null,
    stablecoin_volume_24h  bigint        not null,
    stablecoin_market_cap  bigint        not null,
    derivatives_volume_24h bigint        not null
);

create table if not exists job
(
    id        bigint auto_increment
        primary key,
    timestamp datetime     not null,
    job       varchar(15)  not null,
    success   tinyint(1)   not null,
    duration  time(3)      not null,
    error     varchar(150) null
);

create table if not exists marketcap
(
    id                      smallint auto_increment
        primary key,
    timestamp               datetime       not null,
    symbol                  varchar(13)    not null,
    name                    varchar(40)    not null,
    price                   decimal(20, 2) not null,
    marketcap               bigint         not null,
    marketcap_dominance     decimal(7, 2)  null,
    rank_delta              smallint       null,
    high                    decimal(20, 2) null,
    high_percentage         decimal(7, 2)  null,
    high_timestamp          timestamp      null,
    `1d_price_change`       decimal(20, 2) null,
    `1d_price_change_pct`   decimal(7, 2)  null,
    `1d_volume`             bigint         null,
    `1d_volume_change_pct`  decimal(7, 2)  null,
    `7d_price_change`       decimal(20, 2) null,
    `7d_price_change_pct`   decimal(7, 2)  null,
    `7d_volume`             bigint         null,
    `7d_volume_change_pct`  decimal(7, 2)  null,
    `30d_price_change`      decimal(20, 2) null,
    `30d_price_change_pct`  decimal(7, 2)  null,
    `30d_volume`            bigint         null,
    `30d_volume_change_pct` decimal(7, 2)  null,
    sparkline               json           null
);

create table if not exists pnl
(
    id                mediumint auto_increment
        primary key,
    timestamp         datetime       not null,
    current           decimal(20, 2) not null,
    current_btc       decimal(14, 6) not null,
    current_24h       decimal(7, 2)  null,
    current_btc_24h   decimal(7, 2)  null,
    binance_total     decimal(20, 2) not null,
    binance_total_btc decimal(14, 6) not null,
    binance_total_24h decimal(7, 2)  null,
    bitmex_total      decimal(20, 2) not null,
    bitmex_total_btc  decimal(14, 6) not null,
    bitmex_total_24h  decimal(7, 2)  null,
    pnl               decimal(10, 2) null,
    pnl_binance       decimal(10, 2) null,
    pnl_bitmex        decimal(10, 2) null,
    pnl_cum           decimal(7, 2)  null,
    constraint pnl_ix_id
        unique (id)
);

create table if not exists portfolio
(
    id                               mediumint auto_increment
        primary key,
    timestamp                        datetime               not null,
    btc_usd                          decimal(20, 2)         not null,
    eth_usd                          decimal(20, 2)         not null,
    current                          decimal(20, 2)         not null,
    current_btc                      decimal(14, 6)         not null,
    current_24h                      decimal(7, 2)          null,
    current_1w                       decimal(7, 2)          null,
    current_btc_24h                  decimal(7, 2)          null,
    current_btc_1w                   decimal(7, 2)          null,
    current_percentage               decimal(7, 2)          not null,
    total                            decimal(20, 2)         not null,
    total_btc                        decimal(14, 6)         not null,
    total_24h                        decimal(7, 2)          null,
    total_1w                         decimal(7, 2)          null,
    total_btc_24h                    decimal(7, 2)          null,
    total_btc_1w                     decimal(7, 2)          null,
    binance_total                    decimal(20, 2)         not null,
    binance_total_btc                decimal(14, 6)         not null,
    binance_total_24h                decimal(7, 2)          null,
    binance_total_1w                 decimal(7, 2)          null,
    binance_count                    smallint               null,
    bitmex_total                     decimal(20, 2)         not null,
    bitmex_total_btc                 decimal(14, 6)         not null,
    bitmex_total_24h                 decimal(7, 2)          null,
    bitmex_total_1w                  decimal(7, 2)          null,
    bitmex_margin                    double(20, 2)          not null,
    bitmex_margin_24h                decimal(7, 2)          null,
    bitmex_margin_1w                 decimal(7, 2)          null,
    bitmex_margin_btc                decimal(14, 6)         not null,
    bitmex_margin_percent            decimal(7, 2)          not null,
    bitmex_margin_leverage           decimal(20, 2)         not null,
    bitmex_available_margin          decimal(20, 2)         not null,
    bitmex_available_margin_btc      decimal(14, 6)         not null,
    bitmex_unrealised                decimal(20, 2)         null,
    bitmex_unrealised_24h            decimal(10, 2)         null,
    bitmex_unrealised_1w             decimal(15, 2)         null,
    bitmex_unrealised_btc            decimal(14, 6)         null,
    bitmex_unrealised_percentage     decimal(7, 2)          null,
    bitmex_withdraw                  decimal(20, 2)         null,
    bitmex_withdraw_btc              decimal(14, 6)         null,
    bitmex_btc_position              double(20, 2)          null,
    bitmex_btc_position_btc          decimal(14, 6)         null,
    bitmex_btc_position_24h          decimal(7, 2)          null,
    bitmex_btc_position_percentage   decimal(7, 2)          null,
    bitmex_btc_position_type         enum ('LONG', 'SHORT') null,
    bitmex_btc_position_leverage     double(4, 2)           null,
    bitmex_btc_position_opening      decimal(20, 2)         null,
    bitmex_btc_position_opening_date datetime               null,
    bitmex_eth_position              decimal(20, 2)         null,
    bitmex_eth_position_btc          decimal(14, 6)         null,
    bitmex_eth_position_24h          decimal(7, 2)          null,
    bitmex_eth_position_percentage   decimal(7, 2)          null,
    bitmex_eth_position_type         enum ('LONG', 'SHORT') null,
    bitmex_eth_position_leverage     decimal(4, 2)          null,
    bitmex_eth_position_opening      decimal(20, 2)         null,
    bitmex_eth_position_opening_date datetime               null,
    atari_total                      decimal(8, 2)          null,
    atari_total_btc                  decimal(8, 6)          null,
    atari_usd                        decimal(6, 2)          null,
    atari_rank                       smallint               null,
    atari_rank_delta                 smallint               null,
    atari_1d                         decimal(7, 2)          null,
    atari_1d_volume                  decimal(7, 2)          null,
    atari_7d                         decimal(7, 2)          null,
    atari_7d_volume                  decimal(7, 2)          null,
    atari_30d                        decimal(7, 2)          null,
    atari_30d_volume                 decimal(7, 2)          null,
    constraint portfolio_ix_id
        unique (id)
);

create table if not exists test
(
    id  int auto_increment
        primary key,
    val varchar(100) null
);

create table if not exists ucts
(
    id           smallint auto_increment
        primary key,
    timestamp    datetime   not null,
    btc_2h       smallint   not null,
    btc_2h_side  varchar(4) not null,
    btc_2h_date  date       not null,
    btc_4h       smallint   not null,
    btc_4h_side  varchar(4) not null,
    btc_4h_date  date       not null,
    btc_8h       smallint   not null,
    btc_8h_side  varchar(4) not null,
    btc_8h_date  date       not null,
    btc_12h      smallint   not null,
    btc_12h_side varchar(4) not null,
    btc_12h_date date       not null,
    btc_1d       smallint   not null,
    btc_1d_side  varchar(4) not null,
    btc_1d_date  date       not null,
    eth_2h       smallint   not null,
    eth_2h_side  varchar(4) not null,
    eth_2h_date  date       not null,
    eth_4h       smallint   not null,
    eth_4h_side  varchar(4) not null,
    eth_4h_date  date       not null,
    eth_8h       smallint   not null,
    eth_8h_side  varchar(4) not null,
    eth_8h_date  date       not null,
    eth_12h      smallint   not null,
    eth_12h_side varchar(4) not null,
    eth_12h_date date       not null,
    eth_1d       smallint   not null,
    eth_1d_side  varchar(4) not null,
    eth_1d_date  date       not null
);

create table if not exists worker
(
    id           smallint auto_increment
        primary key,
    timestamp    datetime    not null,
    lifetime     varchar(20) not null,
    working_time varchar(20) not null,
    successful   mediumint   not null,
    failed       mediumint   not null
);

