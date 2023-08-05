import os
import numpy as np
import tensorflow as tf
from sklearn.utils import shuffle as shuffle_data
from ..layers import Dense
from .callbacks import EarlyStopping
from .losses import *
from .metrics import *
from .optimizers import *


class Model(object):
    def __init__(self,
                 name='model',
                 reset_graph=True):
        if reset_graph:
            tf.reset_default_graph()

        self._name = name if name is not None else ''
        self._layers = []
        self._shapes = []
        self._sess = None
        self._restored = False

    def __del__(self):
        if self._sess is not None:
            self._sess.close()

    @property
    def layers(self):
        return self._layers

    def add(self, layer):
        input_dim = layer.input_dim
        output_dim = layer.output_dim

        if input_dim is None:
            if len(self.layers) == 0:
                raise AttributeError('input_dim must be specified '
                                     'on first layer.')
            else:
                layer.input_dim = self._shapes[-1][1]

        if output_dim is None:
            layer.initialize_output_dim()

        self._shapes.append(layer.shape)
        self._layers.append(layer)

    def compile(self, loss='mse', optimizer='rmsprop',
                variable_input=False,
                use_mask=False,
                pad_value=0):
        if not self._restored:
            self._compile_layers()

        if not variable_input:
            input_shape = [None] + list(self.layers[0].input_shape)
        else:
            input_shape = [None] + [None] * len(self.layers[0].input_shape)
        output_shape = [None] + list(self.layers[-1].output_shape)

        x = self.data = \
            tf.placeholder(self.layers[0].input_dtype,
                           shape=input_shape, name='x')
        t = self.target = \
            tf.placeholder(self.layers[-1].output_dtype,
                           shape=output_shape, name='t')

        if use_mask:
            mask = tf.cast(tf.not_equal(x, pad_value), tf.float32)
        else:
            mask = None

        training = self.training = \
            tf.placeholder_with_default(False, ())

        y = self._y = self._predict(x, training=training, mask=mask)
        self._loss = self._compile_loss(loss, y, t)
        self._train_step = \
            self._optimize(optimizer).minimize(self._loss)

        if not self._restored:
            self._sess = tf.Session()
            self._init = tf.global_variables_initializer()
            self._sess.run(self._init)
        else:
            uninitialized_variables = [
                var for var in tf.global_variables()
                if var.name.split(':')[0].encode()
                in set(self._sess.run(tf.report_uninitialized_variables()))
            ]
            self._sess.run(tf.variables_initializer(uninitialized_variables))

    def describe(self):
        layers = self.layers
        digits = int(np.log10(len(layers))) + 1
        for i, layer in enumerate(layers):
            print('#{}: {}'.format(str(i).zfill(digits), layer))

    def describe_params(self):
        layers = self.layers
        digits = int(np.log10(len(layers))) + 1
        for i, layer in enumerate(layers):
            _params = layer.params
            print('-' * 48)
            print('#{}: {}'.format(str(i).zfill(digits), layer))
            print('-' * 48)
            if len(_params) == 0:
                print('No params')
            else:
                for j, param in enumerate(_params):
                    print('{}: {}'.format(param.name,
                                          param.get_shape()))
            if i == len(layers) - 1:
                print('-' * 48)

    def eval(self, elem, feed_dict):
        return self._sess.run(elem, feed_dict=feed_dict)

    def fit(self, data, target,
            epochs=10, batch_size=100,
            validation_data=None,
            metrics=[],
            preprocesses=[],
            shuffle=True,
            early_stopping=-1,
            verbose=1):

        if len(data) != len(target):
            raise AttributeError('Length of X and y does not match.')

        es = None
        if early_stopping > -1:
            if validation_data is None:
                raise AttributeError('early_stopping needs validation_data.')
            es = EarlyStopping(patience=early_stopping, verbose=verbose)

        n_data = len(data)
        if n_data < batch_size:
            batch_size = n_data
        n_batches = n_data // batch_size

        for epoch in range(epochs):
            results = [['loss', 0.]]

            if shuffle:
                indices = shuffle_data(np.arange(n_data))
                _data = data[indices]
                _target = target[indices]
            else:
                _data = data
                _target = target

            for i in range(n_batches):
                _start = i * batch_size
                _end = _start + batch_size

                _batch_data = _data[_start:_end]
                _batch_target = _target[_start:_end]

                for _preprocess in preprocesses:
                    _batch_data = _preprocess(_batch_data)

                self.eval(self._train_step,
                          feed_dict={
                              self.data: _batch_data,
                              self.target: _batch_target,
                              self.training: True
                          })
                results[0][1] += self.loss(_batch_data, _batch_target)

                if verbose:
                    for j, metric in enumerate(metrics):
                        _res = self.metric(metric, _batch_data, _batch_target)
                        if i == 0:
                            results.append(_res)
                        else:
                            results[j+1][1] += _res[1]

            if validation_data is not None:
                val_data = validation_data[0]
                for _preprocess in preprocesses:
                    val_data = _preprocess(val_data)
                val_target = validation_data[1]
                val_loss = self.loss(val_data, val_target)

            if verbose:
                def _format(results):
                    return ', '.join(map(lambda tup:
                                     '{}: {:.3}'.format(tup[0], tup[1]),
                                         results))

                out = 'epoch: {}, '.format(epoch + 1)
                for i, res in enumerate(results):
                    results[i][1] /= n_batches

                out += _format(results)

                if validation_data is not None:
                    out += ', '
                    results = [('val_loss', val_loss)]
                    for metric in metrics:
                        results.append(self.metric(metric,
                                                   val_data,
                                                   val_target,
                                                   validation=True))
                    out += _format(results)
                print(out)
            if es is not None:
                if es.on_epoch_end(epoch, val_loss):
                    break

    def predict(self, data):
        ret = self.eval(self._y,
                        feed_dict={
                            self.data: data
                        })
        return ret

    def loss(self, data, target):
        loss = self.eval(self._loss,
                         feed_dict={
                            self.data: data,
                            self.target: target
                         })
        return loss

    def metric(self, metric, data, target, validation=False):
        metrics = {
            'accuracy': ('acc', self.accuracy),
            'f1': ('f1', self.f1),
            'precision': ('pre', self.precision),
            'recall': ('rec', self.recall)
        }

        if metric in metrics:
            name = metrics[metric][0]
            score = metrics[metric][1](data, target)
        else:
            name = 'custom'
            score = metric(data, target)

        if validation:
            name = 'val_' + name

        if not validation:
            return [name, score]
        else:
            return (name, score)

    def accuracy(self, data, target):
        return accuracy(self.predict(data), target)

    def f1(self, data, target):
        return f1(self.predict(data), target)

    def precision(self, data, target):
        return precision(self.predict(data), target)

    def recall(self, data, target):
        return recall(self.predict(data), target)

    def restore(self, model_path):
        if self._sess is not None:
            raise AttributeError('Session alrady initialized. '
                                 'Model variables must be restored '
                                 'before compile.')
        self._compile_layers()
        self._sess = tf.Session()
        saver = tf.train.Saver()
        saver.restore(self._sess, model_path)
        self._restored = True

    def save(self, out_path, verbose=1):
        out_dir = out_path.split('/')[:-1]
        if len(out_dir) > 0:
            os.makedirs(os.path.join(*out_dir), exist_ok=True)
        saver = tf.train.Saver()
        saver.save(self._sess, out_path)

        if verbose:
            print('Model saved to: \'{}\''.format(out_path))

    def _compile_layers(self):
        with tf.variable_scope(self._name):
            for layer in self._layers:
                layer.compile()

    def _compile_loss(self, loss, data, target):
        losses = {
            'binary_crossentropy': binary_crossentropy,
            'categorical_crossentropy': categorical_crossentropy,
            'mean_squared_error': mean_squared_error,
            'mse': mean_squared_error
        }

        if loss in losses:
            cost = losses[loss](data, target)
        else:
            cost = loss(data, target)

        for layer in self._layers:
            cost += tf.reduce_sum(layer.reg_loss)

        return cost

    def _predict(self, x, **kwargs):
        output = x
        for layer in self.layers:
            output = layer.forward(output, **kwargs)

        return output

    def _optimize(self, optimizer):
        optimizers = {
            'adadelta': adadelta,
            'adagrad': adagrad,
            'adam': adam,
            'momentum': momentum,
            'rmsprop': rmsprop,
            'sgd': sgd
        }

        if optimizer in optimizers:
            return optimizers[optimizer]()
        else:
            return optimizer()
