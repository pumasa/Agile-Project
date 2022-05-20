import json
import os
import cv2

class Image:
    def __init__(self, uploaded_file, recipeID):
        self.recipeID = recipeID
        self.imagesrc = ''
        self.file = uploaded_file

    def verify_file_type(self):
        if str(self.file).endswith('jpg') or str(self.file).endswith('jpeg'):
            return True
        if str(self.file).endswith('png') or str(self.file).endswith('bmp'):
            return True
        return False

    def store(self):
        if self.verify_file_type():
            image_dir = self.return_path("../static/images")
            self.imagesrc = f'{image_dir}/{str(self.file)}'

            cv2.imwrite(self.file, self.imagesrc)

    def save(self):
        to_json = self.to_json()
        csv_path = self.return_path("../database/image.json")
        file_data = self.load_database()
        
        file_data.append(to_json)
        with open(csv_path, "w") as f:
            json.dump(file_data, f, indent=1)

    def to_json(self):
        json = {
            f"recipeID": self.recipeID,
            f"imagesrc": self.imagesrc
        }

        return json
    
    def return_path(self,given_path):
        cwd = os.path.abspath(os.path.dirname(__file__))
        csv_path = os.path.abspath(os.path.join(cwd, given_path))
        return csv_path 

    def load_database(self):
        csv_path = self.return_path("../database/image.json")
        with open(csv_path, "r") as f:
            file_data = json.loads(f.read())
        return file_data

    

    