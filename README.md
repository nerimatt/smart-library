# Smart Library

esp to control various sensors in my library

## connect to usb serial
![circuit](https://techtotinker.com/wp-content/uploads/2020/10/MP_013_UART.png)
we dont need to connect 5v, it will be provided byu library, so we can debug on pc while library is powered by wall plug

## todo
* move all data/ to sd card
* cluster in sd put current state, so if its fill(3,2,0) or fade with options when it boots up it remembers
* cluster put mutexes to edit
* at boot, load config and save in memory to be globally accessible (see if it is doable)
* find way to upload to sd card, move alarms there
* add motion sensors
* add light sensor to dim lights
* add microphone -> dance mode make led reactive to sound
