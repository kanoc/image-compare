import os
from datetime import datetime
from typing import List

from flask import request, render_template, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from app import app
from app.db import db
from app.db.models import Image
from app.alg import extract_features, best_matches


ALLOWED_CONTENT_TYPES = {'image/png', 'image/jpeg'}


@app.route('/')
def index():
    """The main page."""

    return render_template('index.html')


@app.route('/upload_image', methods=['POST'])
def upload_image():
    """Upload an image."""

    index_page = url_for('index')
    # Do some sanity checks.
    if 'image' not in request.files:
        flash('No file received')
        return redirect(index_page)
    image_file = request.files['image']
    if not image_file or not image_file.filename:
        flash('No file selected')
        return redirect(index_page)
    if image_file.content_type not in ALLOWED_CONTENT_TYPES:
        flash('Selected file must be a PNG or JPG')
        return redirect(index_page)

    # Validation done, save the file.
    image_filename = secure_filename(image_file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    image_file.save(image_path)
    # Extract the feature vector.
    feature_vector: List[float] = list(extract_features(image_path))
    # Write the image data to the database.
    image_data = Image(filename=image_filename, date_uploaded=datetime.now(), feature_vector=feature_vector)
    db.session.add(image_data)
    db.session.commit()

    return redirect((url_for('matching_images', image_id=image_data.id)))


@app.route('/image/<string:filename>', methods=['GET'])
def image(filename: str):
    """Serve a given image."""

    return send_from_directory(app.config['UPLOAD_FOLDER'], secure_filename(filename))


@app.route('/matching_images/<int:image_id>', methods=['GET'])
def matching_images(image_id: int):
    """Search for matching images for the given image"""

    base_image: Image = Image.query.get_or_404(image_id, 'Image not found')
    other_images: List[Image] = Image.query.filter(Image.id != base_image.id).all()
    best_matching_images: List[Image] = []

    if other_images:
        best_matching_images = best_matches(base_image, other_images)
    return render_template('matching_images.html', base_image=base_image, matching_images=best_matching_images)
