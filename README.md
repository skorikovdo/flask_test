# **Problem statement**

In this problem, you should build a messaging system. The system involves the
following entities:

(a) Users: A user has a unique ID and a list of the user IDs that they "follow."

(b) Messages: A message has a unique ID, the user ID who posted the message, the
    message body (a text string), a timestamp, and an optional 'in-reply-to'
    message ID.

(c) Timeline: A timeline is a sorted list of messages that are "interesting" for
    a given user. Timelines are sorted by message timestamp (descending). A
    message M appears in the timeline of user X iff M was authored by a user
    that user X follows AND:
    (1) M's in-reply-to field is nil, OR
    (2) M's in-reply-to field is N, message N is authored by user Y, and user X
        follows user Y


#### Your system should support the following operations:

(a) Post(X, Y): Post message X as user Y

(b) Follow(X, Y): User X now follows user Y

(c) Unfollow(X, Y): User X no longer follows user Y

(d) Timeline(X, K): Return the first (most recent) K messages of the timeline of
    user X

<br/>
You do not need to provide a GUI or web interface; rather, your solution should
provide an implementation of the interface (API) shown above.
You should also provide some example code, or unit tests that illustrates the usage of your API.

<br/>
Language

Python is preferred, but other programming language are allowed (although
  compilation and usage instructions should be included as described above)
 Your solution can use standard library packages -- third-party libraries and
  packages should generally be avoided.



# Solution

```

POST /api/user/create - завести пользоваталя, передаем параметр 'name',
формате json (прим. {"name":"Pavel"}), при успешной записи вернет код 200.

GET /api/user/list - вернет список всех пользователей.

GET /api/user/1 - вернет пользователя с id = 1.

POST /api/followers/create - подписаться/отписаться от пользователя.
Передаем параметры id подписчка, и id на кого подписываемся
(прим. {"follower_id": "1", "followed_id": "4"} - пользователь с id = 1
подписался на пользователя с id = 4. При повторной отправке произойдет
отписка пользователя).

GET /api/followers/list - выводит пользователя и его подписчиков

POST /api/message/create - завести сообщение. Передаем параметры id
пользователя, который является втором сообщения, и текст сообщения.
(прим. {"user_id":"1", "message_text": "Hello"})

POST /api/message/post - Передаем id автора сообщений, получаем список
его сообщений (прим. {"id":1} - вернет все сообщений пользования с
id == 1)

POST /api/message/list - Передаем id подписчика, получаем
список сообщений от пользователей на которых подписаны. Список отфильтрован
сначала свежие сообщения

```
