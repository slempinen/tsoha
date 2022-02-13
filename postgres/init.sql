CREATE TABLE account
(
    id serial not null,
    username varchar(50) not null,
    password varchar(50) not null,
    constraint user_pk primary key (id)
);
