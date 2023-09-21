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
* - _mode_: '**r**' for random interval or '**f**' for fixed interval
