import app
import os

path = "database/samples/"
images_name = os.listdir(path)
filename = "samples_template"
app.serializes(images_name, path, filename)


path = "database/permitted/"
images_name = os.listdir(path)
filename = "permitted_template"
app.serializes(images_name, path, filename)


