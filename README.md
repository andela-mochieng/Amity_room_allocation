##Amity Room Allocation

**Clone this repo**

```shell
$ git clone  https://github.com/margierain/Amity_room_allocation.git.
````

Fetch from develop-branch
```shell
$ git checkout develop
```

Navigate to the root folder

Install packages required

## Launching the program
```shell
$ Run python run.py --launch, -l
```

*This causes an (Amity)prompt to appear.*

##### *To create muiltiple living or office spaces*

```shell
$ (Amity) create_rooms <room_name>...
```
###### To add person to a room

```shell
$ (Amity)add_person  <person_fname> <person_lname>(FELLOW|STAFF) [--wa=n]
```

##### Command to reallocate person from one room to another

##### Enables user to load people from a file to a db
```shell
$ (Amity) load_people
```

##### View everyone allocated in rooms

```shell
$ (Amity) print_allocations [--o=filename]
```

##### view people unallocated
```shell
$ (Amity) print_unallocated [--o=filename]
```

##### View people allocated to a room
```shell
(Amity) print_room <room_name>
```

#### Read everything from the db and load it to the terminal
```shell
$ (Amity) load_state <amity.sqlite>
```

###### Get a review of all the comands
```
$ (Amity) (-h | --help)```




