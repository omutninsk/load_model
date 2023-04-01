from randimage import get_random_image
import matplotlib, io

class RandomImage():
    def __init__(self, x,y):
        self.x = x
        self.y = y
    
    def generate(self):
        img_size = (self.x,self.y)
        img = get_random_image(img_size)
        image_bytes = io.BytesIO()
        matplotlib.image.imsave(image_bytes, img)
        image_bytes.seek(0)
        return image_bytes