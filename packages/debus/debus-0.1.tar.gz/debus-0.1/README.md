## cybus: DBus with cython

## How?
CyBus runs dbus using asyncio event loop, no extra (runtime)dependencies or foreign eventloops required.

## Why?


## Really, why?
Well, for work I wanted to run some python code on a specific device and didn't want to cross-compile glib&co (actually, they are present on the device, but vendor patched them in a funny way and I didn't want to use them).
And I was pretty tired of always forgetting where that lib for "import gi" comes from.

Then one slightly boring weekend happened.

## Known limitations

 - Only little-endian messages are supported so far
 - Methods have to return a tuple to match dbus idea of multiple "out" parameters
 - Lack of maturiy (yeah, something from a random dude with only a couple of months of history)