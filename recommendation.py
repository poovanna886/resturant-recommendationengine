from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
from pyspark import SparkContext as sc


ratings = list(map(lambda x : Rating(x[0],x[1],x[2]), [(1,1,100),(1,2,3),(1,3,3),
           (2,1,0),(2,2,4),(2,3,2),
           (3,1,100),(3,2,2),(3,2,1)]))
ratings = sc.parallelize(ratings)

# Build the recommendation model using Alternating Least Squares
rank = 3
numIterations = 10
model = ALS.train(ratings, rank, numIterations)

# Evaluate the model on training data
testdata = ratings.map(lambda p: (p[0], p[1]))
predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
ratesAndPreds = ratings.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
print("Mean Squared Error = " + str(MSE))
