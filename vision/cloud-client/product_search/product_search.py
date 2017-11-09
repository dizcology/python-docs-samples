#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Demonstrates product catalog management and product search API.

Example usage:
  ...
"""
# [START imports]
import argparse
import io

from google.cloud import vision_v1
from google.cloud import vision_v1alpha1

from google.cloud.vision_v1alpha1 import types
# [END imports]

def create_catalog():
    """Creates a catalog.

    Note: For v1alpha1, a catalog will not be returned by ``ListCatalogs`` until reference images have been added to it. Therefore it's important that you note the catalog name returned by the ``CreateCatalog`` request as it is required for adding reference images.
    """
    client = vision_v1alpha1.ProductSearchClient()

    # alternatively: catalog = {}
    catalog = types.Catalog()

    catalog = client.create_catalog(catalog)
    print('Catalog created: {}'.format(catalog))

    return catalog


def delete_catalog(catalog_name):
    """Deletes a catalog."""
    client = vision_v1alpha1.ProductSearchClient()
    client.delete_catalog(catalog_name)


def import_catalog(csv_file_uri):
    client = vision_v1alpha1.ProductSearchClient()

    gcs_source = types.ImportCatalogsGcsSource(csv_file_uri=csv_file_uri)
    input_config = types.ImportCatalogsInputConfig(gcs_source=gcs_source)

    operation = client.import_catalogs(input_config=input_config)

    return operation


def create_reference_image(catalog_name, image_uri, product_id):
    # enums.ProductSearchCategory
    category_names = ('PRODUCT_SEARCH_CATEGORY_UNSPECIFIED', 'SHOES', 'BAGS')

    client = vision_v1alpha1.ProductSearchClient()
    reference_image = types.ReferenceImage(image_uri=image_uri, product_id=product_id)

    reference_image = client.create_reference_image(parent=catalog_name, reference_image=reference_image)

    print('Reference image created: {}'.format(reference_image.name))
    print('Category: {}'.format(category_names[reference_image.category]))


def list_reference_images(catalog_name, prouct_id=None):
    # enums.ProductSearchCategory
    category_names = ('PRODUCT_SEARCH_CATEGORY_UNSPECIFIED', 'SHOES', 'BAGS')

    client = vision_v1alpha1.ProductSearchClient()

    reference_images = client.list_reference_images(parent=catalog_name, product_id=product_id)

    for reference_image in reference_images:
        print('Name: {}'.format(reference_image.name))
        print('Category: {}'.format(category_names[reference_image.category]))
        print('Image URI: {}'.format(reference_image.image_uri))
        print('Product ID: {}\n'.format(reference_image.product_id))


def get_reference_image(reference_image_name):
    # enums.ProductSearchCategory
    category_names = ('PRODUCT_SEARCH_CATEGORY_UNSPECIFIED', 'SHOES', 'BAGS')

    client = vision_v1alpha1.ProductSearchClient()

    reference_image = client.get_reference_image(name=reference_image_name)

    print('Name: {}'.format(reference_image.name))
    print('Category: {}'.format(category_names[reference_image.category]))
    print('Image URI: {}'.format(reference_image.image_uri))
    print('Product ID: {}\n'.format(reference_image.product_id))


def delete_reference_image(reference_image_name):
    client = vision_v1alpha1.ProductSearchClient()

    client.delete_reference_image(name=reference_image_name)


def delete_reference_images(catalog_name, product_id):
    client = vision_v1alpha1.ProductSearchClient()

    client.delete_reference_images(parent=catalog_name, product_id=product_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    args = parser.parse_args()
