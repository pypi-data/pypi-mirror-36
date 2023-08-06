# PyC8

Welcome to the GitHub page for **pyC8**, a Python driver for the Digital Edge Fabric.

## Features


- Clean Pythonic interface.
- Lightweight.

## Compatibility

- Python versions 3.4, 3.5 and 3.6 are supported.

## Build & Install

To build,

```bash
 $ python setup.py build
```
To install locally,

```bash
 $ python setup.py build
```

## Package and Make available through pip

Requirements,

```bash
 $ python3 -m pip install --user --upgrade setuptools wheel
 $ python3 -m pip install --user --upgrade twine
```

Run following command from directory where setup.py is present.

```base
 $ python3 setup.py sdist bdist_wheel
```

Initally Upload the Distribution to Test Archives test.pypi.org for testing purposes. This step will prompt you for username and password.

* username: `macrometaco`
* password: `poweruser!@#`

```bash
 $ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
The above test distribution you uploaded can be installed using:

```bash
 $ pip3 install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pyc8
```

Upload the Distribution Archives to pip.org. This step will prompt you for username and password.

* username: `macrometaco`
* password: `poweruser!@#`

```bash
 $ twine upload dist/*
```

You may need to use `sudo` depending on your environment.

## Getting Started

Here is a multi-tenancy example:

```python

    from c8 import C8Client

    # Initialize the client for C8DB.
    client = C8Client(protocol='http', host='localhost', port=8529)

    # Connect to "_system" database as root user in tenant "_mm".
    sys_tenant = client.tenant(name='_mm', dbname='_system', username='root', password='poweruser')

    # List all the tenants and DC list
    sys_tenant.tenants()
    sys_tenant.dclist()
    sys_tenant.dclist_local() # Get local tenant DC list

    # Create a new database named 'firefly'.
    sys_tenant.create_tenant('firefly')

    # Use newly created tenant 'firefly'.
    tennt = client.tenant(name='firefly', dbname='_system', username='root', password='')

    # Add new tenant user "captain_mal".
    tennt.create_user(username="captain_mal", password='', active=True)

```

```python

    from c8 import C8Client

    # Initialize the client for C8DB.
    client = C8Client(protocol='http', host='localhost', port=8529)

    sys_tenant = client.tenant(name='_mm', dbname='_system', username='root', password='poweruser')

    # Connect to "_system" database as root user.
    sys_db = client.db(name='_system', username='root', password='poweruser')

    # Create a new database named "test in all DC. The dcl is pulled ".
    dcl = sys_tenant.dclist()
    sys_db.create_database('test', dclist=dcl)

    # Connect to "test" database as root user.
    db = client.db(name='test', username='root', password='')

    # Create a new collection named "students".
    students = db.create_collection('students')

    # Add a hash index to the collection.
    students.add_hash_index(fields=['name'], unique=True)

    # Insert new documents into the collection.
    # Insert vertex documents into "students" (from) vertex collection.
    students.insert({'_key': 'STUD01', 'name': 'Jean-Luc Picard'})
    students.insert({'_key': 'STUD02', 'name': 'James T. Kirk'})
    students.insert({'_key': 'STUD03', 'name': 'Han Solo'})

    # Execute a C8QL query and iterate through the result cursor.
    cursor = db.c8ql.execute('FOR doc IN students RETURN doc')
    student_names = [document['name'] for document in cursor]

    print("Student names inserted: " + str(student_names))

```

Here is another example with graphs:

```python

    from c8 import C8Client

    # Initialize the client for C8DB.
    client = C8Client(protocol='http', host='localhost', port=8529)

    # Connect to "test" database as root user.
    db = client.db('test', username='root', password='passwd')

    # Create a new graph named "school".
    graph = db.create_graph('school')

    # Create vertex collections for the graph.
    students = graph.create_vertex_collection('students')
    lectures = graph.create_vertex_collection('lectures')

    # Create an edge definition (relation) for the graph.
    register = graph.create_edge_definition(
        edge_collection='register',
        from_vertex_collections=['students'],
        to_vertex_collections=['lectures']
    )

    # Insert vertex documents into "students" (from) vertex collection.
    students.insert({'_key': '01', 'full_name': 'Anna Smith'})
    students.insert({'_key': '02', 'full_name': 'Jake Clark'})
    students.insert({'_key': '03', 'full_name': 'Lisa Jones'})

    # Insert vertex documents into "lectures" (to) vertex collection.
    lectures.insert({'_key': 'MAT101', 'title': 'Calculus'})
    lectures.insert({'_key': 'STA101', 'title': 'Statistics'})
    lectures.insert({'_key': 'CSC101', 'title': 'Algorithms'})

    # Insert edge documents into "register" edge collection.
    register.insert({'_from': 'students/01', '_to': 'lectures/MAT101'})
    register.insert({'_from': 'students/01', '_to': 'lectures/STA101'})
    register.insert({'_from': 'students/01', '_to': 'lectures/CSC101'})
    register.insert({'_from': 'students/02', '_to': 'lectures/MAT101'})
    register.insert({'_from': 'students/02', '_to': 'lectures/STA101'})
    register.insert({'_from': 'students/03', '_to': 'lectures/CSC101'})

    # Traverse the graph in outbound direction, breadth-first.
    result = graph.traverse(
        start_vertex='students/01',
        direction='outbound',
        strategy='breadthfirst'
    )
```

Example for Stream Collections:

```python
    from c8 import C8Client

    # Initialize the client for C8DB.
    client = C8Client(protocol='http', host='localhost', port=8529)

    sys_tenant = client.tenant(name='_mm', dbname='_system', username='root', password='poweruser')

    # Connect to "_system" database as root user.
    sys_db = client.db(name='_system', username='root', password='poweruser')
    
    #Create a new global persistent stream called test-stream. If persistent flag set to False,
    # a non-persistent stream gets created. Similarly a local stream gets created if local 
    # flag is set to True. By default persistent is set to True and local is set to False . 
    sys_db.create_stream('test-stream', persistent=True, local=False)
    
    #List all persistent/non-persistent and global/local streams 
    streams = sys_db.streams()
    
    #Create producer for the given persistent/non-persistent and global/local stream.
    stream_collection = sys_db.stream()
    producer = stream_collection.create_producer('test-stream', persistent=True, local=False)
    
    #Send: is a plusar method that publish/sends a given message over stream in byte's.
    producer.send(b"Hello")
    
    #Create a subscriber to the given persistent/non-persistent and global/local stream with the given,
    # subscription name. If no subscription new is provided then a random name is generated. based on
    # tenant and db information
    subscriber = stream_collection.subscribe('test-stream', persistent=True, local=False, subscription_name="test-subscription")
    
    #receive: is a plusar function to read the published messages over stream.
    subscriber.receive()
    
    #Delete a given persistent/non-persistent and global/local stream.
    sys_db.delete_stream('test-stream', persistent=True, local=False)
```