## Installation
`$ pip3 install ftredis`

## Usage
```python
from ftredis import Client

r = Client(namespace='prefix', decode_responses=True)

# redis commands
r.set('key', 'value')
r.get('key')
r.delete('key')

# create index
r.ftcreate('name', 'text', 'weight', 3.0, 'desc', 'text')

# add documents
r.ftadd('doc-1', name='qwe', desc='some sample text')
r.ftadd('doc-2', name='asd', desc='some sample text')
r.ftadd('doc-3', name='zxc', desc='some sample text')

# delete documents
r.ftdel('doc-1')

# search
r.ftsearch('sample -@name:asd', 'nocontent', 'limit', 0, 3)

# drop index
r.ftdrop()
```