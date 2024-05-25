import unittest
import pyweb


class TestAssertion(unittest.TestCase):
    def test_assertion(self):
        self.assertEqual(1, 1)


# class TestImageViewer(unittest.TestCase):
#     def test_image_viewer(self):
#         # Define list of testable image file types
#         # TODO: Add more image file types to this list: "gif", "bmp", "tiff", "svg", "pdf"
#         file_types = ["jpg", "png", "webp"]

#         for type in file_types:
#             # Path to the test image
#             test_image_path = f"tests/test_images/test_image.{type}"

#             # Call the main function with the test image
#             pyweb.main(test_image_path)


if __name__ == "__main__":
    unittest.main()
