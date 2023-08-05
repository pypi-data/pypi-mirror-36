from keras.models import load_model

import pickle

import numpy


class Model:
    def __init__(self, model_path = None):
        """Initializes a neural network model.

        If you want to load a model you've already trained, just give a path of model file.
        
        Keyword Arguments:
            model_path {str} -- A path of model file. (default: {None})
        
        Raises:
            e -- Raises error when loading a model is failed.
        """
        if type(model_path) == type(None):
            self.model = None
        else:
            try:
                self.model = load_model(model_path)
                self.input_shape = self.model.input_shape[1:]
                if type(self.model) == type(None):
                    print('Nothing loaded')
            except Exception as e:
                print('Model loading failed')
                raise e

    def save(self, model_path):
        """Saves a model as h5 format.
        
        Arguments:
            model_path {str} -- Path to save model.
                
        Raises:
            TypeError -- Raises error if self.model is not created.
            e -- Raises error if a path is wrong.
        """
        try:
            if type(self.model) == type(None):
                raise TypeError('you should create a model before save it')
            self.model.save(model_path)
        except Exception as e:
            raise e

    def set_output_dictionary(self, output_dictionary):
        self.model.output_dictionary = output_dictionary
        self.model.__class__.output_dictionary = self.model.output_dictionary

    def compile_model(self, optimizer, loss=None, metrics=['accuracy']):
        """This function compiles self.model according to arguments.
        
        Arguments:
            optimizer {str or keras optimizer instance} -- See https://keras.io/optimizers/ for more information about optimizers.
        
        Keyword Arguments:
            loss {str or objective function} -- See https://keras.io/losses/ for more information about loss. (default: {None})
            metrics {list} -- List of metrics to be evaluated by the model during training and evaluating(testing). (default: {['accuracy']})
        """
        self.model.compile(optimizer, loss=loss, metrics=metrics)    

    def predict(self, data_array, predict_classes = True):
        """Generates output of predictions for the input samples.
        
        Arguments:
            data_array {ndarray} -- The input data like x_test of keras.
        
        Keyword Arguments:
            predict_classes {bool} --
                Decides a prediction result's type.
                By default, a return value of prediction result is an array of classes.
                If you set predict_classes as False, you can get a raw output array as a prediction result.
                (default: {True})

        Raises:
            e -- Raise exception when prediction failed.
        
        Returns:
            [ndarray] -- Predicted classes(labels) of input data
        """
        try:
            probs = self.model.predict(data_array)
            if predict_classes == False:
                return probs
            predicted_classes = probs.argmax(axis=-1)
            try:
                for i in range(predicted_classes.shape[0]):
                    if i == 0:
                        return_list = [ self.model.output_dictionary[predicted_classes[i]] ]
                    else:
                        return_list.append( self.model.output_dictionary[predicted_classes[i]] )
                return numpy.asarray(return_list)
            except:
                return predicted_classes
        except Exception as e:
            # Prediction failed
            raise e

    def print_summary(self):
        self.model.summary()