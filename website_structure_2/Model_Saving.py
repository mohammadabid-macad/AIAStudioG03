import tensorflow as tf

# Define your model here
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(18,)),
    tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.Dense(1, activation='linear')
])

# Compile your model here
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mse'])

# Save the model in HDF5 format
model.save('material_texture_classifier_correct.h5', save_format='h5')
