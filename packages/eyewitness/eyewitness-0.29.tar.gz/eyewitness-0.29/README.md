# EyeWitness
Lightweight Framework for ObjectDetection.
wrapper your own detector and add your handler.

system design:
https://drive.google.com/file/d/1x_sCFs91swHR1Z3ofS4e2KFz6TK_kcHb/view?usp=sharing


## env
implement with python3.6, i.e. detector should support python3.6, too.


## Installation
```bash
pip install eyewitness
```


## TODO
- survey CI, CD integration with gitlab
- add image producer(restricted with ImageId)
- add examples using more model(wrapper with docker, survey for lightweight/ more accurate model)
- add image_puller for image collection. (consumer design)


## Things to be consider
[scale up]
- queuing system (how images pass(bytes(do by producer), file(queuing in fs))
- multiple detector


## unit-test
```
nose2
```

a flake flask object detection example:
```
# start a server at http://localhost:5566/
# you can implement your own ObjectDetector, DetectionResultHandler
python run_flask_server.py

# post pikachu image bytes to flask server
# which will stores raw pikachu and drawn pikachu.png at workspace
curl -X POST \
  http://localhost:5566/detect_image_byte \
  -H 'content-type: application/json' \
  -H 'store_image_path: ./pikachu_raw.png' \
  --data-binary "@eyewitness/test/pics/pikachu.png"

# post by channel
curl -X POST \
  http://localhost:5566/detect_image_byte \
  -H 'content-type: application/json' \
  -H 'channel: pikachu' \
  -H 'file-format: png' \
  --data-binary "@eyewitness/test/pics/pikachu.png"


# post path of existing pikachu image file to flask server
# which will stores drawn pikachu.png at workspace
curl -X POST \
  http://localhost:5566/detect_image_file \
  -H 'content-type: application/json' \
  -H 'image_path: ./eyewitness/test/pics/pikachu.png'
```


## Real Detector example
please take look at docker/RFB_detector/README.md
which is eyewitness example that wrapper a detection model
