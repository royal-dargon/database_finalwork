drop database if exists `BlogStore`;
create database `BlogStore`;
use `BlogStore`;

create table `user_info` (
    `id` int auto_increment comment "用户id",
    `uname` varchar(10) not null comment "用户的昵称",
    `pwd` varchar(30) not null comment "用户登录密码",
    `gender` boolean not null comment "用户性别",
    `email` varchar(40) not null comment "用户的邮箱信息",
    `mark` int not null comment "用户的等级信息",
    primary key(`id`)
) ENGINE = InnoDB DEFAULT CHARSET = UTF8MB4;

insert into user_info (uname, pwd, gender, email, mark) values ('zk', '1111', 1, '23125@qq.com', 1);

create table `manager` (
    `id` int auto_increment comment "管理员id",
    `mname` varchar(10) not null comment "管理员昵称",
    `gender` boolean not null comment "管理员性别",
    `pwd` varchar(30) not null comment "管理员密码",
    `email` varchar(40) not null comment "管理员邮箱",
    primary key(`id`)
) ENGINE = InnoDB DEFAULT CHARSET = UTF8MB4;

insert into manager (mname, gender, pwd, email) values ('txn', 1, '2222', '96545@qq.com'); 

create table `user_power` (
    `user_id` int not null comment "用户id",
    `grade` int not null comment "用户权限等级",
    `file_size` int not null comment "用户上传文件最大值",
    `release_cap` int not null comment "每日上传日志的最大值",
    `watermark` boolean not null comment "是否拥有水印的权力",
    `ecode` boolean not null comment "是否拥有加锁的权利",
    primary key(`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = UTF8MB4;

insert into user_power (user_id, grade, file_size, release_cap, watermark, ecode) values (1, 1, 100, 5, 1, 0);

create table `manager_power` (
    `manager_id` int not null comment "管理员id",
    `grade` int not null comment "管理员权限等级",
    `log` boolean not null comment "是否拥有对日志或评论管理权力",
    `photo` boolean not null comment "是否拥有对照片管理权力",
    `muser` boolean not null comment "是否拥有对用户管理权力",
    `message` boolean not null comment "是否拥有发布公告的权力",
    `model` boolean not null comment "是否拥有对模板管理的权力",
    primary key(`manager_id`)
) ENGINE = InnoDB DEFAULT CHARSET = UTF8MB4;

insert into manager_power (manager_id, grade, log, photo, muser, message, model) values (1, 1, 1, 1, 1, 1, 1);

create table `model` (
    `model_id` int auto_increment not null comment "模板id",
    `content` varchar(100) not null comment "模板内容信息",
    `grade` int not null comment "模板等级",
    `price` float not null comment "模板价格",
    primary key(`model_id`)
) ENGINE = InnoDB DEFAULT CHARSET = UTF8MB4;

create table `log_info` (
    `log_id` int auto_increment not null comment "日志id",
    `model_id` int not null comment "日志使用的模板id",
    `user_id` int not null comment "日志发布者id",
    `title` varchar(20) not null comment "日志标题",
    `content` text not null comment "日志正文",
    `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    primary key(`log_id`)
) ENGINE = InnoDB DEFAULT CHARSET = UTF8MB4;

create table `comment_info` (
    `comment_id` int auto_increment not null comment "评论id",
    `log_id` int not null comment "所属日志id",
    `user_id` int not null comment "发布者id",
    `context` text not null comment "评论内容",
    `creat_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    primary key(`comment_id`)
) ENGINE = InnoDB DEFAULT CHARSET = UTF8MB4;

create table `photo` (
    `photo_id` int auto_increment not null comment "照片id",
    `user_id` int not null comment "所属用户id",
    `purl` varchar(40) not null comment "照片url",
    primary key(`photo_id`)
) ENGINE = InnoDB DEFAULT CHARSET = UTF8MB4;

create table `message` (
    `message_id` int auto_increment not null comment "公告id",
    `title` varchar(20) not null comment "公告标题",
    `content` text not null comment "公告正文",
    `creat_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    primary key(`message_id`)
) ENGINE = InnoDB DEFAULT CHARSET = UTF8MB4;

create table `blacklist` (
    `user_id` int not null comment "用户id",
    primary key(`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = UTF8MB4;

create table `model2user` (
    `id` int auto_increment not null,
    `model_id` int not null comment "模板id",
    `user_id` int not null comment "用户id",
    primary key(`id`)
) ENGINE = InnoDB DEFAULT CHARSET = UTF8MB4;