# EyeWitness

## env
implement with python3.6, i.e. detector should support python3.6, too.


## TODO
add simple image producer(generate imageid)

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

