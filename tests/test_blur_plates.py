# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
from unittest.mock import MagicMock, call, patch
import unittest

from oricat.blur_plates import _apply_blur, _blur_plates


class TestBlurPlates(unittest.TestCase):

    @patch("oricat.blur_plates.cv2.GaussianBlur")
    def test_apply_blur_blurs_detected_plates(self, func_gaussian_blur):
        logger = MagicMock()
        img = MagicMock()
        plates = [(1, 2, 3, 4)]
        func_gaussian_blur.return_value = "blurred"

        result = _apply_blur(img, plates, logger, "car.jpg")

        self.assertEqual(result, img)
        logger.info.assert_called_once_with(
            "Found %s plate(s) in %s, blurring...", 1, "car.jpg"
        )
        func_gaussian_blur.assert_called_once()
        self.assertEqual(img.__setitem__.call_count, 1)

    @patch("oricat.blur_plates.cv2.GaussianBlur")
    def test_apply_blur_logs_warning_when_no_plate(self, func_gaussian_blur):
        logger = MagicMock()
        img = MagicMock()

        result = _apply_blur(img, [], logger, "car.jpg")

        self.assertEqual(result, img)
        logger.warning.assert_called_once_with("No plates detected in %s", "car.jpg")
        func_gaussian_blur.assert_not_called()

    def test_blur_plates_processes_supported_images(self):
        logger = MagicMock()
        cascade = MagicMock()
        cascade.detectMultiScale.side_effect = [[(1, 2, 3, 4)], []]

        with patch("oricat.blur_plates.cv2.data.haarcascades", "/cascade/"), patch(
            "oricat.blur_plates.init", return_value=logger
        ), patch("oricat.blur_plates.os.path.exists", return_value=False), patch(
            "oricat.blur_plates.os.makedirs"
        ) as func_makedirs, patch(
            "oricat.blur_plates.os.listdir", return_value=["a.jpg", "b.txt", "c.PNG"]
        ), patch(
            "oricat.blur_plates.os.path.isfile", return_value=True
        ), patch(
            "oricat.blur_plates.cv2.CascadeClassifier", return_value=cascade
        ) as func_cascade_classifier, patch(
            "oricat.blur_plates.cv2.imread", return_value="image"
        ), patch(
            "oricat.blur_plates.cv2.cvtColor", return_value="gray"
        ), patch(
            "oricat.blur_plates.cv2.imwrite"
        ) as func_imwrite, patch(
            "oricat.blur_plates._apply_blur", return_value="blurred-image"
        ) as func_apply_blur:
            _blur_plates("some/in", "some/out")

        func_cascade_classifier.assert_called_once_with(
            "/cascade/haarcascade_russian_plate_number.xml"
        )
        func_makedirs.assert_called_once_with("some/out")
        logger.info.assert_has_calls(
            [
                call("Processing %s images from %s...", 2, "some/in"),
                call("Finished processing %s images to %s", 2, "some/out"),
            ]
        )
        self.assertEqual(func_apply_blur.call_count, 2)
        self.assertEqual(func_imwrite.call_count, 2)

    def test_blur_plates_skips_makedirs_when_output_exists(self):
        logger = MagicMock()

        with patch("oricat.blur_plates.cv2.data.haarcascades", "/cascade/"), patch(
            "oricat.blur_plates.init", return_value=logger
        ), patch("oricat.blur_plates.os.path.exists", return_value=True), patch(
            "oricat.blur_plates.os.makedirs"
        ) as func_makedirs, patch(
            "oricat.blur_plates.os.listdir", return_value=[]
        ), patch(
            "oricat.blur_plates.os.path.isfile", return_value=False
        ), patch(
            "oricat.blur_plates.cv2.CascadeClassifier", return_value=MagicMock()
        ), patch(
            "oricat.blur_plates.cv2.imread", return_value="image"
        ), patch(
            "oricat.blur_plates.cv2.cvtColor", return_value="gray"
        ), patch(
            "oricat.blur_plates.cv2.imwrite"
        ) as func_imwrite, patch(
            "oricat.blur_plates._apply_blur", return_value="blurred-image"
        ) as func_apply_blur:
            _blur_plates("some/in", "some/out")

        func_makedirs.assert_not_called()
        func_imwrite.assert_not_called()
        func_apply_blur.assert_not_called()
