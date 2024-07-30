# Main

## API

### Internal
#### Download API
used to download copys of factorio
#### Matchmaking API
used to get info on current server listings
#### Mod Portal API
used to broswe and download mods from the mod portal
#### Web authentication API
used to get a token that is used in other apis as authentication

### Public
these apis require a API Key made on factorio.com
#### Mod upload API
used to upload new releases of mods to the mod portal
#### Mod details API
used to change mod information like the description on the mod portal
#### Mod images API
used to add, reorder or remove images from mods on the mod portal
#### Mod publish API
used to publish new mods to the mod portal

## Data
### data types/IO
#### Read 
functions that take in bytes and return values, such as reading bytes and returning an int
#### Write
functions that take in values and return bytes, such as taking in ints and returning bytes
### Files
functions and classes to make reading and writing of achievement files and mod settings easy
#### Achievement Files
#### Mod Settings
### Strings
functions and classes to make encoding and decoding of blueprint and map exchange strings easy
#### Blueprints
#### Map exchange



# Timeline
## API
gonna focus on the matchmaking API first since that is what i really want for a project
the public APIs are prob last since i doubt anyone would use those
## Data
### Files
i already got data IO, just got to reorder and make it nice
got a reader and writer for Mod settings, got to reorder and make it nice,  

achievement files seem like it will be annoying but shouldn't be too long

### Strings
not sure if i will do this before or after public APIs, it's not a focus of mine, i guess i will see when i get there



## Order
Port over Mod Setting Reader/Writer that i already made  
<br>
update data IO since i learned a bit more about it   
<br>
Matchmaking API and prob Web authentication API because of how small it is   
### stuff after this is unordered
Blueprint and Map exchange strings   
Achievement files  
Internal APIs  
Public APIs   
make sure everything looks good  
examples and who knows what else   




