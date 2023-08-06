# MongoODM

MongoODM is a rediculously simple wrapper around the pymongo and mongomock libraries to provide a way to classify your documents (and test them)

## Example Use
The following is a way you can use the odm and switch dbs on the fly:
```
from mongoodm import MongoODM, Document

uri = 'mongodb://localhost:27017'
db = MongoODM(uri=uri)

uri2 = 'mongodb://localhost:26015'
db2 = MongoODM(uri=uri2)

class User(Document):
    pass

# Get documents from the first db
print(db(User).all())

# Get Documents from the second db
print(db2(User).all())
```

Here's a simple example of creating a class and using it:
```
from mongoodm import MongoODM, Document

class User(Document):
    pass

# This will raise an exception because the db hasn't been initialised
User.find({})

db = MongoODM() # Connects to localhost by default

# This now works
User.find({})
```

If you're used to Django style models here's another way you can use:
```
from mongoodm import MongoODM

db = MongoODM()

class User(db.Document):
    pass

User.find_one({})
```

Have you got flask? You can setup the config values in your app config:
 - `MONGOODM_URI` uri of the mongo instance
 - `MONGOODM_PROVIDER` the provider you want to use (mongomock or pymongo)

```
from flask import Flask
from mongoodm import MongoODM
app = Flask(__name__)
db = MongoODM(app=app)

class User(db.Document):
    pass

@app.route('/')
def hello_world():
    user = User.find_one({'_id': 'me'})
    return 'Hello, %s!' % User.name
```

## Notes
This readme is still being updated as the library is still in flux. There are things that I don't like about this implementation, namely that the following happens:

```
db = MongoODM()
db2 = MongoODM(uri='mongodb://notlocalhost:32768')

class User(db.Document):
    pass

# This will return results from db2
User.all({})
```

I'll likely have to dynamically subclass Document or something akin to that so that this doesn't happen.
