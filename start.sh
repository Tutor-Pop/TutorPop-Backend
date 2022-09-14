echo "[PROJECT] Git pulling..."
git pull

echo "[PROJECT] Pulling completed. Pathing to virtual-environment..."
source ./env/Scripts/activate || source ./env/bin/activate

echo "[PROJECT] Install any dependencies..."
pip install -r requirements.txt

echo "[PROJECT] All set. Starting TutorPop-Backend project..."
python manage.py runserver