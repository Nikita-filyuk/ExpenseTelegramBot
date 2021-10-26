create table category(
    codename varchar(255) primary key,
    name varchar(255),
    aliases text
);

create table expense(
    id integer primary key,
    rubles integer,
    created datetime,
    category_codename varchar,
    user varchar(255),
    message text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name, aliases)
values
    ('products', 'продукты', 'еда'),
    ('dinner', 'обед', 'роллы, покушали, кфс, мак, бк'),
    ('transport', 'транспорт', 'такси, автобус, самолет, самокат, каршеринг'),
    ('car', 'машина', 'машина, октаха, ремонт, бензин'),
    ('energy', 'энергетик', 'энергетик, берн, адреналин'),
    ('clothes', 'одежда', 'одежда, эйчик, вещи'),
    ('other', 'прочее', '');