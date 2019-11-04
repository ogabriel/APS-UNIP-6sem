# temporario

import app

images_name = ['101_1.tif', '102_1.tif', '103_1.tif'] # achar um jeito de puxar isso automatico
path = "database/permitted/"
filename = "samples_processed"
app.serializes(images_name, path, filename)