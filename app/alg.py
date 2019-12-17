"""The algorithm for extracting and comparing images based on image features.

Adapted from: https://medium.com/machine-learning-world/feature-extraction-and-similar-image-search-with-opencv-for-
newbies-3c59796bf774
"""

import logging
from typing import List, Optional

import cv2
import numpy as np
from scipy import spatial
from imageio import imread

from app.db.models import Image


logger = logging.getLogger(__name__)


def extract_features(image_path: str, vector_size: int = 64) -> Optional[np.array]:
    """Extract the relevant image features for the given image.

    :param image_path: Full path to the image.
    :param vector_size: The size of the feature vector
    :return: The extracted feature vector.
    """
    image = imread(image_path)
    try:
        alg = cv2.AKAZE_create()
        # Finding image keypoints.
        keypoints = alg.detect(image)
        # Number of keypoints varies depending on image size and color pallet.
        # Sorting them based on keypoint response value(bigger is better).
        keypoints = sorted(keypoints, key=lambda x: x.response, reverse=True)[:vector_size]
        # Computing descriptors vector.
        keypoints, desc_vector = alg.compute(image, keypoints)
        # Flatten all of them in one big vector - our feature vector.
        desc_vector = desc_vector.flatten()
        # Making descriptor of same size. Descriptor vector size is 64.
        needed_size = (vector_size * 64)
        if desc_vector.size < needed_size:
            # If we have less descriptors than needed, just add zeros at the end of the feature vector.
            desc_vector = np.concatenate([desc_vector, np.zeros(needed_size - desc_vector.size)])
        # Return the computed feature vector.
        return desc_vector
    except cv2.error as exc:
        logger.error('Failed to extract image features: %s', exc)
        return None


def best_matches(base_image: Image, other_images: List[Image], max_results: int = 2) -> List[Image]:
    """Search for the best matching images for the given base image.

    :param base_image: Search for images similar to this one.
    :param other_images: Search for similar images from this pool.
    :param max_results: Return this many matches.
    :return: The found similar images sorted in descending order based on similarity ranking.
    """
    # Calculate the cosine distance between the feature vector of the base image and the other images.
    bi_feature_vector = np.array(base_image.feature_vector)
    o_feature_vectors = np.array([i.feature_vector for i in other_images])
    base_feature_vector = bi_feature_vector.reshape(1, -1)
    img_distances = spatial.distance.cdist(o_feature_vectors, base_feature_vector, 'cosine').reshape(-1)
    # Get the top n records.
    nearest_ids = np.argsort(img_distances)[:max_results].tolist()
    return [other_images[image_index] for image_index in nearest_ids]
