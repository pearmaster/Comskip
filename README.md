## Comskip

Commercial detector
http://www.kaashoek.com/comskip/ and https://github.com/erikkaashoek/Comskip

This fork focuses on the repackaging into a docker image.

It includes a comskip.ini for my USA setup.

It also includes a python webserver which handles the queuing and execution of videos.

You can, for example, start this docker image in the same docker network as emby, where the two containers share the same media volume, and then the emby post-process script queues the video for comskip.
