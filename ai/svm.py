import tensorflow as tf
import numpy as np
import scipy.io as io
from matplotlib import pyplot as plt

# nie weim po co to jest
# from tensorflow.python.framework import ops
# ops.reset_default_graph()




# dataset = tf.placeholder(shape=[None, ])

filename_queue = tf.train.string_input_producer(["generatedDataset.csv"])
reader = tf.TextLineReader()
key, value = reader.read(filename_queue)
record_defaults = [[1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], ["none"]]
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15, col16, col17 = tf.decode_csv(value, record_defaults=record_defaults)
features = tf.stack([col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15, col16])

# create graph
with tf.Session() as sess:
    # Start populating the filename queue.
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)


    for i in range(1):
        # Retrieve a single instance:
        example, label = sess.run([features, col17])
        print example, label

    coord.request_stop()
    coord.join(threads)

    # DODAC SHUFFLE
