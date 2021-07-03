from architecture import *
from imutils import paths
img_path=sorted(list(paths.list_images("dataset")))
random.seed(42)
random.shuffle(img_path)
data=[]
lbl=[]
print ("There are ",len(img_path), " images in the dataset")
print ("Loading each images..")
print ("Please wait..")
for i,imgs in enumerate(img_path):
    img=cv2.imread(imgs)
    img=cv2.resize(img,(500,500))
    lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_image)
    median = cv2.medianBlur(l,5)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(median)
    n = cv2.merge([cl, a, b])
    data.append(np.array(img).flatten())
    if "noacc" in imgs.lower():
        c1=0
    else:
        c1=1
    lbl.append(int(c1))
x=np.array(data)
y=np.array(lbl)
print(x)
print(y)

createArc()
