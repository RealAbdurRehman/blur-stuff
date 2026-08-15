import os

os.environ["FLAGS_use_mkldnn"] = "0"
os.environ["FLAGS_use_onednn"] = "0"

import paddle

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
