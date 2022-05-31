drop database if exists BlogStore;
create database BlogStore;
use BlogStore;

drop table if exists user_info;
create table user_info (
    id serial,
    uname varchar(10) not null,
    pwd varchar(30) not null,
    gender boolean not null,
    email varchar(40) not null,
    mark int not null,
    primary key(id)
);

insert into user_info (uname, pwd, gender, email, mark) values ('zk', '1111', 1, '23125@qq.com', 1);

create table manager(
    id serial,
    mname varchar(10) not null,
    gender boolean not null,
    pwd varchar(30) not null,
    email varchar(40) not null,
    primary key(id)
);

insert into manager (mname, gender, pwd, email) values ('txn', 1, '2222', '96545@qq.com');

create table user_power(
    user_id int not null,
    grade int not null,
    file_size int not null,
    release_cap int not null,
    watermark boolean not null,
    ecode boolean not null,
    primary key(user_id)
);

insert into user_power (user_id, grade, file_size, release_cap, watermark, ecode) values (1, 1, 100, 5, 1, 0);

create table manager_power(
    manager_id int not null,
    grade int not null,
    log boolean not null,
    photo boolean not null,
    muser boolean not null,
    message boolean not null,
    model boolean not null,
    primary key(manager_id)
);

insert into manager_power (manager_id, grade, log, photo, muser, message, model) values (1, 1, 1, 1, 1, 1, 1);

create table model(
    model_id serial not null,
    content varchar(100) not null,
    grade int not null,
    price float not null,
    primary key(model_id)
);

create table log_info(
    log_id serial not null,
    model_id int not null,
    user_id int not null,
    title varchar(20) not null,
    content text not null,
    create_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    primary key(log_id)
);

create table comment_info(
    comment_id serial not null,
    log_id int not null,
    user_id int not null,
    context text not null,
    creat_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    primary key(comment_id)
);

create table photo(
    photo_id serial not null,
    user_id int not null,
    purl varchar(40) not null,
    primary key(photo_id)
);

create table message(
    message_id serial not null,
    title varchar(20) not null,
    content text not null,
    creat_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    primary key(message_id)
);

create table blacklist(
    user_id int not null,
    primary key(user_id)
);

create table model2user(
    id serial not null,
    model_id int not null,
    user_id int not null,
    primary key(id)
);