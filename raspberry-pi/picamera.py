from picamera2 import Picamera2


class Camera:
    def __init__(self):
        _picam = Picamera2()
        self._configure_camera()

    def _configure_camera(self):
        camera_config = self.picam.create_preview_configuration()
        self.picam.configure(camera_config)

    def capture_image(self, filename):
        self.picam.start()
        self.picam.picam.capture_file(filename)

    def close_camera(self):
        self.picam.close()
