* Problem statement
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

Your system should support the following operations:

(a) Post(X, Y): Post message X as user Y
(b) Follow(X, Y): User X now follows user Y
(c) Unfollow(X, Y): User X no longer follows user Y
(d) Timeline(X, K): Return the first (most recent) K messages of the timeline of
    user X

You do not need to provide a GUI or web interface; rather, your solution should
provide an implementation of the interface (API) shown above.
You should also provide some
- example code, or
- unit tests that illustrates the usage of your API.

* Language
- Python is preferred, but other programming language are allowed (although
  compilation and usage instructions should be included as described above)
- Your solution can use standard library packages -- third-party libraries and
  packages should generally be avoided.

* Readme
Include a README with your submission. The README should describe
- how to compile (if necessary) and run your submission on a recent Linux/OS X machine
- your high-level design
- notable design decisions you made
- situations in which your design would or would not be suitable for example
- how does your design scale as a function of the number of users, the size of follower lists, the rate at which new messages are posted, and the rate (and K-value) of timeline
requests?