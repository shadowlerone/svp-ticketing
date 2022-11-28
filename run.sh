# python -m venv venv
# . venv/bin/activate
# pip install .  # install your application
pip install -r Requirements
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0 'app:app'