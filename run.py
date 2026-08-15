import os

os.environ["FLAGS_use_mkldnn"] = "0"

import paddle

print("FLAGS_use_mkldnn:", paddle.get_flags(["FLAGS_use_mkldnn"]))

print("=== PADDLE DEBUG ===")
print("Version:", paddle.__version__)
print("Device:", paddle.device.get_device())
print("Paddle:", paddle.__file__)

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
