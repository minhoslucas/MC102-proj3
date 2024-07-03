import os

CLASSMATE_SPRITES_FOLDER = os.path.join('assets', 'images', 'classmate_sprites')
classmate_sprites_list = []

for file in os.scandir(CLASSMATE_SPRITES_FOLDER):
    classmate_sprites_list.append(file.path)