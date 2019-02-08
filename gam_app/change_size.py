file = '164e1a37-50d8-4b5f-9244-2ac3d9b38b1a-017_005_001_001.jpg'
location = file.split('-')[-1]
location = location.split('.')[0]
physical_location = location
# print(physical_location)
# print(location)
location = location.split('_')
box = location[0]
# print(box)
bundle = location[1]
# print(bundle)
folder = location[2]
# print(folder)
image = location[3]
# print(image)

parts = file.split('-')[:-1]
uuid = ''
for i in parts:
    uuid += i + '-'
print(uuid[:-1])
