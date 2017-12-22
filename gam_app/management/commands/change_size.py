from PIL import Image
#https://stackoverflow.com/questions/13407717/python-image-library-pil-how-to-compress-image-into-desired-file-size
class file_counter(object):
    def __init__(self):
        self.position = self.size = 0

    def seek(self, offset, whence=0):
        if whence == 1:
            offset += self.position
        elif whence == 2:
            offset += self.size
        self.position = min(offset, self.size)

    def tell(self):
        return self.position

    def write(self, string):
        self.position += len(string)
        self.size = max(self.size, self.position)

def smaller_than(im, size, guess=70, subsampling=1, low=1, high=100):
    while low < high:
        counter = file_counter()
        im.save(counter, format='JPEG', subsampling=subsampling, quality=guess)
        if counter.size < size:
            low = guess
        else:
            high = guess - 1
        guess = (low + high + 1) // 2
    return low

def change_size_if_needed(file):
    if os.path.getsize(file) > 4000000:
        im = Image.open(file)
        size = smaller_than(im,4000000)
        im.save(file, 'JPEG', quality=size)
