## Intro
A toy Flask app for having fun with some simple images comparision algorithms.


## Required packages

Make sure you have installed:
 * ``docker`` (tested with v18.09.7)
 * ``docker-compose`` (tested with v1.17.1)


## Usage

1. First time setup
```bash
$ docker-compose run --rm app /bin/bash -c "cd /opt/services/image_compare && python -c  'from app.web import db; db.create_all()'"
```

2. Fire up the cluster
```bash
$ docker-compose up -d
```

3. Browse to localhost:9009 to interact with the app.


## Tests

To run the tests in a virtual env:
1. Create a virtual env with `virtualenv`:
   ```bash
   mkvirtualenv -p /usr/bin/python3.7 image-compare
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

Code quality checks:
```bash
inv check
```

Run the tests:
1. Install the dev requirements with:
    ```bash
    inv deps
    ```
2. Run the tests with coverage report:
    ```bash
    inv test
    ```
3. Run the tests without coverage report:
    ```bash
    inv test --no-coverage
    ```


## Tech stack

It's a dead simple `Flask` web app with a very simple `Bootstrap` based UI.

The image matching algorithm uses ``imageio`` to read the image files and ``OpenCV`` and ``SciPy`` to do the image
processing.


## Notes on the image similarity algorithm

After trying (and failing) to come up with my own "homebrew" algorithm, I ended up using a feature detection based
approach described here:

https://medium.com/machine-learning-world/feature-extraction-and-similar-image-search-with-opencv-for-newbies-3c59796bf774

I did some minor tweaks (switching from KAZE to AKAZE and making it work with the latest lib versions). In essence
the image matching works like this:

1. When an image is uploaded, a 64 keypoints based feature vector is extracted from it and stored in a database (with
some other basic image info)

2. After the image is saved, the feature vector of the newly uploaded image is compared to all other existing feature
vectors in the database (by measuring the "spatial" cosine distance between the feature vectors), and the 3 best matches
are shown on the UI.

The results are pretty average at best, but it was a fun ride!