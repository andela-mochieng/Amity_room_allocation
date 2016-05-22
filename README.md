[![Build Status](https://travis-ci.org/andela-mochieng/Amity_room_allocation.svg?branch=develop)](https://travis-ci.org/andela-mochieng/Amity_room_allocation)
[![Coverage Status](https://coveralls.io/repos/github/andela-mochieng/Amity_room_allocation/badge.svg?branch=develop)](https://coveralls.io/github/andela-mochieng/Amity_room_allocation?branch=develop)

##Amity Room Allocation

>This is a a console application allocate offices and living spaces at Amity to Andela employees.

**__Clone this repo__**
```shell
$ https://github.com/margierain/Amity_room_allocation.git.
```

**__Fetch from develop-branch__**

```
$ git checkout develop
```

**__Navigate to the root folder__**
```shell
$ cd Amity_room_allocation
```

**__Install packages required__**
```shell
$ pip install  -r requirements.txt
```


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

```shell
$ (Amity) reallocate_person  <person_fname> <person_lname> <new_room_name>
```

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
```shell
$ (Amity) (-h | --help)
```

**watch the functionality**
[![asciicast](https://asciinema.org/a/ecf1yzu8gvhiwwtg5ry4fuoil.png)](https://asciinema.org/a/ecf1yzu8gvhiwwtg5ry4fuoil)




