# ############################## Start the webserver, the opencv color grabber and the GUI #############################

from threading import Thread
from vision import grab_colors
background_thread = Thread(args=(8080, 20, 2))
background_thread.start()
# Server listens now on port 8080, maxlength 20 moves, timeout 2 seconds
thr = Thread(target=grab_colors)
thr.start()
# Run the opencv code and detect facelet colors

import gui
# Start the GUI with several sliders to configure some opencv parameters

