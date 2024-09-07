echo "Changing to tamagotchi directory"
cd ~/projects/python/tamagotchi/

echo "Stashing any previous changes"
git stash

echo "Pulling from master"
git pull origin master

echo "Complete!"

echo "Launching Tamagotchi"
python3 tamagotchi.py
