# cosmic_raiders
A relatively sophisticated game for the Numwroks calculator inspired by those arcade space invader games. 

## Install
Go to https://my.numworks.com/python/ccsio/cosmic_raiders
Make sure your calculator is plugged in
Click the "Load to Calculator" button


## Custom Levels
All levels have to be appended to the 'levels' variable.
A level is a tuple with **two** sub-tuples, each containing **8** items.
An item is either a **tuple** containing data for that ship, or **'dead'** indicating no ship.
Structure of the data for the ship: (_ship name_,_class data_,_movement data_)

### Basic Ship
* _ship name_: 'basic'
* _class data_: None


### Tank Ship
* _ship name_: 'tank'
* _class data_: None

### Shooter Ship
* _ship name_: 'shooter'
* _class data_: 3-item tuple
  - _mode_: '**r**' for random interval or '**f**' for fixed interval
  - _param_: for **r**: shoot chance (1/x, default: 115), for **f**: interval in seconds
  - _bullet speed_: speed of the bullet (px/update, default: 5)
 
### Ram (Kamikaze) Ship
* _ship name_: 'ram'
* _class data_: 2-item tuple
  - _mode_: **r**: random, **f**: fixed interval
  - _param_: for **r**: ram chance, for **f**: interval
* _movement data_: **mandatory**
  - _axis_: **y**
  - _distance_: **180** for top row, **140** for bottom row
  - _px/update_: multiple of _distance_ (default: 12)
  - _loop?_: **True**
  - _wait_time_: time waiting before coming back up (in seconds)

### Shield Ship
* _ship name_: 'shield'
* _class data_: 3-item tuple
  - _shield chance_: chance to shield/update (deafult: 200)
  - _shield time_: time of active shield (in seconds)
  - _ships_: # of ships shielded (max 5 if in backrow)

### Movement
* any ship can move
* last atribute in ship tuple _ship name_,_class data_,_movement data_)
* _axis_: **x** or **y**
* _distance_: distance covered in px, (Note: no ship colliding prevention!)
* _px/update_: px per update, should be a mulitple of _distance_
* _loop?_: **True** or **False**
* __wait time_: time spent waiting before going back (if applicable) in seconds


