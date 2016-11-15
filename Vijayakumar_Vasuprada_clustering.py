import sys
import numpy as np
import math
import operator

buying = {'vhigh':4.0,'high':3.0,'med':2.0,'low':1.0}
maint = {'vhigh':4.0,'high':3.0,'med':2.0,'low':1.0}
doors = {'2':1.0,'3':2.0,'4':3.0,'5more':4.0}
persons = {'2':1.0,'4':2.0,'more':3.0}
lug_boot = {'small':1.0,'med':2.0,'big':3.0}
safety = {'low':1.0,'med':2.0,'high':3.0}

def get_labels(point):
    label_point = []
    for k,v in buying.iteritems():
        if v == point[0]:
            label_point.append(k)
    for k,v in maint.iteritems():
        if v == point[1]:
            label_point.append(k)
    for k,v in doors.iteritems():
        if v == point[2]:
            label_point.append(k)
    for k,v in persons.iteritems():
        if v == point[3]:
            label_point.append(k)
    for k,v in lug_boot.iteritems():
        if v == point[4]:
            label_point.append(k)
    for k,v in safety.iteritems():
        if v == point[5]:
            label_point.append(k)
    label_point.append(point[6])
    return label_point

def transform_values(l):
    tranformed = []
    if l[0] in buying.keys():
        tranformed.append(buying[l[0]])
    else:
        print "Cannot Recognize Label"
    if l[1] in maint.keys():
        tranformed.append(maint[l[1]])
    else:
        print "Cannot Recognize Label"
    if l[2] in doors.keys():
        tranformed.append(doors[l[2]])
    else:
        print "Cannot Recognize Label"
    if l[3] in persons.keys():
        tranformed.append(persons[l[3]])
    else:
        print "Cannot Recognize Label"
    if l[4] in lug_boot.keys():
        tranformed.append(lug_boot[l[4]])
    else:
        print "Cannot Recognize Label"
    if l[5] in safety.keys():
        tranformed.append(safety[l[5]])
    else:
        print "Cannot Recognize Label"

    # Class Information
    tranformed.append(l[6].strip())

    return tranformed


def getDistance(point1,point2):

    sum = 0.0

    for index in range(len(point1) - 1):
        sum += math.pow((point1[index] - point2[index]),2)
    return math.sqrt(sum)


def assignCluster(initial_centroids,input_points_transformed):
    dict_cluster = {}

    for key in initial_centroids:
        dict_cluster[key] = []

    for point in input_points_transformed:
        minDist = sys.maxint
        minCluster = None
        for key in initial_centroids:
            dist = getDistance(point, key)

            if dist < minDist:
                minDist = dist
                minCluster = key
        dict_cluster[minCluster].append(point)

    return dict_cluster

def getCenter(values):

    centers = [0,0,0,0,0,0]

    for point in values:
        for index in range(len(point) - 1):
            centers[index] += point[index]

    for index in range(len(centers)):
        centers[index] = centers[index]/len(values)

    return centers

def kmeans(initial_centroids,input_points_transformed,k,iter):
    dict_cluster = assignCluster(initial_centroids.keys(),input_points_transformed)
    #previousCentroids = sorted(dict_cluster.keys())

    newCentroids = None
    count = 1
    while count < iter:
        count += 1
        newCentroids = []
        for key,values in dict_cluster.iteritems():
            center = getCenter(values)
            newCentroids.append(tuple(center))
        #print sorted(newCentroids)
        dict_cluster = assignCluster(newCentroids, input_points_transformed)

    return dict_cluster


def kmeans_new(initial_centroids,input_points_transformed,k,iter):

    data_points = input_points_transformed
    centroid_list = initial_centroids.keys()
    dict_cluster = assignCluster(centroid_list,data_points)
    previousCentroids = None

    count = 1
    while previousCentroids != centroid_list and count < iter:
        count += 1
        previousCentroids = centroid_list
        centroid_list = []
        #previousCentroids.sort()
        for entry in previousCentroids:
            points = dict_cluster[entry]
            new_centroid = getCenter(points)
            centroid_list.append(tuple(new_centroid))
        #print sorted(centroid_list)
        dict_cluster = assignCluster(centroid_list, input_points_transformed)

    return dict_cluster


def main(argv):
    k = int(argv[3])
    #k = 4
    iter = int(argv[4])
    #iter = 10
    f = open(argv[1],'r')
    #f = open("input_car",'r')
    f2 = open(argv[2],'r')
    #f2 = open("initialPoints",'r')
    f3 = open("output.txt",'w')

    inputline = f.readlines()
    initial_point_line = f2.readlines()

    input_points_transformed = []
    initial_points_transformed = []

    for line in inputline:
        l = line.split(",")
        new_line = transform_values(l)
        input_points_transformed.append(tuple(new_line))

    # Initial Centroids
    for line in initial_point_line:
        l = line.split(",")
        new_line = transform_values(l)
        initial_points_transformed.append(new_line)

    number_of_features = 6
    initial_centroids = {}

    if k > len(initial_points_transformed):
        k = len(initial_points_transformed)

    for point in initial_points_transformed[0:k]:
        initial_centroids[tuple(point[0:6])] = []


    final_cluster = kmeans(initial_centroids,input_points_transformed,k,iter)
    incorrectly_assigned = 0

    for cluster,points in final_cluster.iteritems():

        class_counter = {'unacc': 0, 'acc': 0, 'good': 0, 'vgood': 0}

        for point in points:
            class_counter[point[6]] += 1

        cluster_name = max(class_counter.iteritems(), key=operator.itemgetter(1))[0]
        #print 'cluster: ' + cluster_name
        f3.write('cluster: ' + cluster_name + '\n')

        for key,item in class_counter.iteritems():
            if key != cluster_name:
                incorrectly_assigned += item

        for point in points:
            original_point = get_labels(point)
            f3.write(str(original_point))
            f3.write('\n')

        f3.write('\n')
        f3.write('\n')

    f3.write('Number of points wrongly assigned:' + '\n')
    f3.write(str(incorrectly_assigned))



if __name__ == '__main__':
    main(sys.argv)