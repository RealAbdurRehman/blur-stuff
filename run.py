import os

os.environ["FLAGS_use_mkldnn"] = "0"

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
