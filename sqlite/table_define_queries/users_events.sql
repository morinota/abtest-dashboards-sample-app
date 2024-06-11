create table users_events (
    user_id int,
    event varchar(32),
    datetime timestamp
);

insert into users_events (user_id, event, datetime)
values 
    (1, 'LAUNCH_APP', '2021-01-01 00:00:00'),
    (1, 'CLICK_BUTTON', '2021-01-01 00:01:00');
