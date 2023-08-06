# clustaar.sqlalchemy is a lightweight postgresql framework based upon sqlachemy


clustaar.sqlalchemy is intended to facilitate and accelerate the use of sqlalchemy. This package allows a quick and easy implementation of a postgresql database. The fact that it is an overlayer of sqlalchemy allows the user to take control at any time and perform complex tasks if necessary.

Another important point is that this package leaves it up to the user to commit these operations whenever he wants. By default, all operation like insertion or deletion of an entry isn't committed but go in a postgresql transaction wich can be later committed.

## Installation

```
pip install clustaar.sqlalchemy
```

## Usage

To begin with, you should perform at least 3 steps.<br>
The first one defines a model that will represent your object.<br>
The second is to define a table that will use the model mentioned above and that defines the future fields of your postgresql table.<br>
The last step is very simple you only have to instantiate the object Database with the connection url of your database and a mapping in the form of a dictionary that will have as key the names of your tables and for value your tables.

After that you would be ready to carry out the operations you wish to do.

### 1) Define a model

```python
class Subscription(object):
    """The class use by the SubscriptionTable """

    def __init__(self, type: str, bot_id: str, user_id: str):
        """
        Args:
            type (str): the subscription type
            bot_id (str): the bot id
            user_id (str): the user id
        """
        self.type = type
        self.bot_id = bot_id
        self.user_id = user_id
```

### 2) Define a table
For this step you have to create your own table class wich extends of the Table class (defined in clustaar.sqlalchemy.table)
As you can see your own table need to implement 2 class property.

_model: store your python model<br>
_shema: store the sqlalchemy table logic<br>

The Schema class take 2 kinds of args:
- the table name
- all your future database column. (For more details see: https://docs.sqlalchemy.org/en/latest/orm/tutorial.html#create-a-schema)

```python
from sqlalchemy import String, Column, Integer
from clustaar.sqlalchemy.schema import Schema
from clustaar.sqlalchemy.table import Table

class SubscriptionTable(Table):
    """ A simple subscription table """

    _model = Subscription
    _schema = Schema("subscriptions",
                     Column("id", Integer, primary_key=True),
                     Column("type", String, nullable=False),
                     Column("bot_id", String, nullable=True),
                     Column("user_id", String, nullable=False))
```

### 3) Define your database
Instanciate the Database class with:
- the database url (ex.: postgresql://scott:tiger@localhost:5432/mydatabase)
- your table mappings

After that you will be able to accest to your subscriptionn table like a porperty (ex.: database.subscriptions).

```python
from os import environ
from clustaar.sqlalchemy.database import Database

database = Database(
    environ["DATABASE_URL"],
    tables={"subscriptions": SubscriptionTable}
)

# You can also create your tables if this is not yet the case
database.setup_all()

```
### 4) Do wath you want

#### [#] Get an entry

You can get an entry in function of many parameters (see clustaar.sqlalchemy.table for more details).

- You have the posibility to get all entry that responds True to the condition.
- You can limit the umber of returned results
- You can limit and/or pagignate your query
- You can order your results
- Use a generator for big query

You can also use large query return with the safe parameter set to True.

If safe parameter is set to True this method use the yield_per sqlalchemy method.<br>
The purpose of this method is when fetching very large result sets (> 10K rows),  to batch results in sub-collections and yield them out partially, so that the Python interpreter doesn’t need to declare very large areas of memory which is both time consuming and leads to excessive memory use

The other important point is the difference in the type of return.<br>
If safe is set to True the return result is an iterator an not a list.

```python
subscriptions = database.subscriptions.get()
subscriptions = database.subscriptions.get(limit=50)
subscriptions = database.subscriptions.get(limit=50, page=5)

# Sort DESC
subscriptions = database.subscriptions.get(sort="-user_id")
# Sort ASC
subscriptions = database.subscriptions.get(sort="+user_id")

# Get subscriptions where type are equal to 'test'
subscriptions = database.subscriptions.get(conditions={"type": "test"})
# Get subscriptions where type doesn't equal to 'test'
subscriptions = database.subscriptions.get(conditions={"type": {"!=": "test"}})


subscriptions = database.subscriptions.get(safe=True)

for subscription in subscriptions:
    do_something(subscription)

```
#### [#] Insert an entry
Just remember the sessions will not be automatically committed.

```python

sub = database.subscriptions.insert(type="test", user_id="56743235", bot_id="456676444")

# does some stuff and when you want commit the transaction.
database.commit()
```

#### [#] Delete and delete_where
Just remember the sessions will not be automatically committed.<br>

'delete_were' use the same conditions as the 'get' method.

```python
sub = database.subscriptions.insert(type="test", user_id="56743235", bot_id="456676444")
database.delete(sub)

sub = database.subscriptions.insert(type="test", user_id="99999999", bot_id="66666666")
database.subscriptions.delete_where(conditions={"user_id": ""99999999""})

# does some stuff and when you want commit the transaction.
database.commit()
```
#### [#] Count entry
You can count the number of entry that responds True to the condition.

```python
database.subscriptions.insert(type="test", user_id="56743235", bot_id="456676444")
database.subscriptions.insert(type="test", user_id="88888888", bot_id="456676444")

num = database.subscriptions.count()

assert num == 2

num = database.subscriptions.count(conditions={"user_id": "77777777"})

assert num == 0
```

#### [#] Bulk insert
Just remember the sessions will not be automatically committed.<br>

You can add many subscription at the same time with bulk insert.

```python
database.subscription.bulk_insert(
    mappings=(
        {"user_id": 1, "bot_id": 2, "type": "pape_news"},
        {"user_id": 2, "bot_id": 2, "type": "pape_news"}
    )
)

# does some stuff and when you want commit the transaction.
database.commit()
```
#### [#] Truncate a table
The truncate method will truncate your table.<br>
For preventing error the session will be automatically committed before and after the truncate.<br>

```python
database.subscriptions.truncate()
```

### 5) Other utils methods on the database object

#### [#] Turn off/on the echo mod
If you want see the sql request you cant turn on the echo mod.

```python

database.echo_turn_on()
database.echo_turn_of()
````

#### [#] Save an entry
Just remember the sessions will not be automatically committed.<br>

You can save an entry easily if it is linked to a maped table.

```python
sub = database.subscriptions.insert(type="test", user_id="56743235", bot_id="456676444")

sub.user_id = "11111111"
database.save(sub)

# does some stuff and when you want commit the transaction.
database.commit()
```

#### [#] Destroy a session
When you want destroy the session (ex: in case of insertion error).

```python
database.remove_session()
```

#### [#] Contextual session
A simple way to perform complex request.<br>
The contextual session let you the possibility to use the native sqlalchemy session in a context manager.<br>

Your request will be automatically committed and the session will be removed to prevent errors.

see https://www.sqlalchemy.org/ for more details.

```python
with database.contextual_session as session:
    data = session.query(Things).filter(Things.c.category.in_(['animal', 'vegetable'])).all()
```

#### [#] Raw query in contextual session
A simple way to perform complex request.<br>
You can easily execute raw SQL queries from a session, using the `execute` mthod.

Your request will be automatically committed and the session will be removed to prevent errors.

see https://www.sqlalchemy.org/ for more details.

```python
with database.contextual_session as session:
    data = session.execute("TRUNCATE TABLE subscriptions")
```
