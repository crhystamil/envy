create table user(
id integer primary key autoincrement,
id_tw text null,
created_at text null,
name text null,
screen_name text null,
profile_image_url text null,
text text null,
location text null,
descripcion text null,
time_zone text null,
friends text null,
json text null
);

create table friends(
id integer primary key autoincrement,
created_at text null,
id_tw text null,
id_u text null,
name text null,
screen_name text null,
profile_image_url text null,
text text null,
location text null,
descripcion text null,
time_zone text null,
friends text null,
status text default 'false',
json text null
);
