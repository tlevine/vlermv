ACID properties
============================
Here's how Vlermv fares in terms of
`database guarantees <https://en.wikipedia.org/wiki/ACID>`_.

Atomicity
    Writes are made to a temporary file that gets renamed.
Consistency
    No validation is supported, so the database is always consistent by definition.
    More seriously, there isn't anything special to handle race conditions, so if
    two threads are writing to the same file, the later one will win.
Isolation
    Vlermv has isolation within files/documents/values but not across. You may implement your own multi-file transactions.
Durability
    All data are saved to disk right away.

Consistency and isolation could be improved with locks, which could be
implemented inside of the vlermv module. This hasn't been an issue for me
because I have been able to design my directory structure such that the
race condition scenarios never occur.

However they are implemented, locks would make vlermv at least somewhat
slower; if I implement some form of transactions in vlermv, I will probably
make them something that you can turn on or off.

If you really need this, I suggest that you wrap vlermv in something that
uses lock files to ensure isolated transactions. 
