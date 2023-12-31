import cv2
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

temp = 0

class DominantColors:
    CLUSTERS = None
    IMAGE = None
    COLORS = None
    LABELS = None

    def __init__(self, image, clusters=3):
        self.CLUSTERS = clusters
        self.IMAGE = image

    def dominantColors(self):
        # read image
        img = cv2.imread(self.IMAGE)

        # convert to rgb from bgr
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # reshaping to a list of pixels
        img = img.reshape((img.shape[0] * img.shape[1], 3))

        # save image after operations
        self.IMAGE = img

        # using k-means to cluster pixels
        kmeans = KMeans(n_clusters=self.CLUSTERS)
        kmeans.fit(img)

        # the cluster centers are our dominant colors.
        self.COLORS = kmeans.cluster_centers_

        # save labels
        self.LABELS = kmeans.labels_

        # returning after converting to integer from float
        return self.COLORS.astype(int)



    #def rgb_to_hex(self, rgb):
    #    return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))



    def plotHistogram(self):
        # labels form 0 to no. of clusters
        numLabels = np.arange(0, self.CLUSTERS + 1)

        # create frequency count tables
        (hist, _) = np.histogram(self.LABELS, bins=numLabels)
        hist = hist.astype("float")
        hist /= hist.sum()

        # appending frequencies to cluster centers
        colors = self.COLORS

        # descending order sorting as per frequency count
        colors = colors[(-hist).argsort()]
        hist = hist[(-hist).argsort()]

        # creating empty chart
        chart = np.zeros((50, 500, 3), np.uint8)
        start = 0

        # creating color rectangles
        for i in range(self.CLUSTERS):
            end = start + hist[i] * 500

            # getting rgb values
            r = colors[i][0]
            g = colors[i][1]
            b = colors[i][2]

            # using cv2.rectangle to plot colors
            cv2.rectangle(chart, (int(start), 0), (int(end), 50), (r, g, b), -1)
            start = end

        # display chart
        plt.figure()
        plt.axis("off")
        plt.imshow(chart)
        plt.show()




if __name__ == '__main__':
    img = r'C:\Users\Rocco\PycharmProjects\TakeCare\green.jpg'
    clusters = 3
    dc = DominantColors(img, clusters)
    colors = dc.dominantColors()



    for i in range(3):
        #red = blood
        if colors[i][0] > 200 and colors[i][1] < 50 and colors[i][2] < 50:
            temp = 6
            print("Blood")
            break
        #green = vaccines
        if colors[i][0] < 50 and colors[i][1] > 200 and colors[i][2] < 100:
            temp = 8
            print("Vaccines")
            break
        #blue = organs
        if colors[i][0] < 50 and colors[i][1] < 200 and colors[i][2] > 200:
            temp = 4
            print("Organs")
            break
    if(temp == 0):
        print("There's no mark. Impossibile to classificate")

    print(temp)

    print(colors)
    dc.plotHistogram()