from keras.callbacks import Callback


class ValidateCallback(Callback):
    '''Create a callback which calculates the accuracy on the validation set in the specified epochs interval

    This speeds-up the training when using heavy validation set.
    '''

    def __init__(self, p, valid_generator, model):
        super().__init__()
        self.param = p
        self.valid_generator = valid_generator
        self.model = model

    def on_epoch_end(self, epoch, logs=None):
        if not epoch % self.param == 0:
            return

        print("Evaluating...")
        scoreSeg = self.model.evaluate_generator(
            generator=self.valid_generator,
            verbose=1,
            workers=8,
        )

        print('Loss: ' + repr(scoreSeg[0]) + ', Acc: ' + repr(scoreSeg[1]))


class SaveCallback(Callback):
    '''Create a callback which saves the model in the specified epochs interval

        This allows you to stop the training whenever you desire.
    '''

    def __init__(self, save_freq, model_path, model):
        super().__init__()
        self.model = model
        self.model_path = model_path
        self.save_freq = save_freq

    def on_epoch_end(self, epoch, logs=None):
        if not epoch % self.save_freq == self.save_freq - 1:
            return

        self.model.save(self.model_path)