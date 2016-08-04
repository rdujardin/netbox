# User scripts

Netbox emits a signal whenever an event occurs in the database : when an object is created, edited or deleted, when a bulk import, edit or delete happens. It also emits a signal whenever accessed directly or through the API, indeed whenever a HTTP request is received.

You can hook your own scripts on these events by putting them in the folder *userscripts* and following the right format. This hook system is based upon the Django's signals system, so all you have to do is connecting receiver functions to the signals you want. You can follow the example already present in *userscripts*, you can also read the [documentation about Django signals](https://docs.djangoproject.com/en/1.9/topics/signals/) to know what is possible to do.

If several receivers are connected to the same signal, possibly in several different scripts, they all will be called when the signal is emitted.

Some parameters are transmitted to the receiver functions : in particular, the concerned class and instance. On a bulk import or bulk delete, individual signals will be emitted : respectively a save and a delete signal will be emitted for each object. Bulk edit works another way : a single signal is emitted for the whole bulk edit, transmitting a parameter *pk_list* containing a list of the concerned primary keys.

For each signal, there are two : a pre and a post.

Your scripts will automatically be loaded if they are in the *userscripts* folder and if they are simple modules. Packages won't be loaded, so if you have heavy treatments to apply to signals you can organize them the way you want in a package and just put next to it a module which will be loaded and which loads the package.

This hooks system can be used to automate your configuration updating from Netbox for instance.
