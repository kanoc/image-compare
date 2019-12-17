"""Tests for the feature extraction and image matching algorithm."""

from datetime import datetime

from app import alg
from app.db.models import Image

from tests import get_fixture_abspath


def test_extract_features():
    # Given an image
    image_path = get_fixture_abspath('image_17.png')
    # Extract the feature vector
    feature_vector = alg.extract_features(image_path, vector_size=64)
    # Make sure the feature vector has the correct length.
    assert len(feature_vector) == 64 * 64


def test_best_matches():
    # Given the base image, the best match end second match
    base_image_filename = 'image_17.png'
    best_match_filename = 'image_1.png'
    second_match_filename = 'image_3.png'
    base_image_path = get_fixture_abspath(base_image_filename)
    best_match_path = get_fixture_abspath(best_match_filename)
    second_match_path = get_fixture_abspath(second_match_filename)
    # Extract the feature vectors
    base_feature_vector = alg.extract_features(base_image_path)
    best_match_feature_vector = alg.extract_features(best_match_path)
    second_match_feature_vector = alg.extract_features(second_match_path)
    # Build he image objects
    base_image = Image(filename=base_image_filename, date_uploaded=datetime.now(), feature_vector=base_feature_vector)
    best_match_image = Image(filename=base_image_filename, date_uploaded=datetime.now(),
                             feature_vector=best_match_feature_vector)
    second_match_image = Image(filename=base_image_filename, date_uploaded=datetime.now(),
                               feature_vector=second_match_feature_vector)
    # Make sure the best match comes out on top.
    found_best_match_image = alg.best_matches(base_image, [best_match_image, second_match_image], max_results=1)[0]
    assert found_best_match_image == best_match_image
