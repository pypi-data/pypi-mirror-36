"""Thompson Sampling with linear posterior over a learnt deep representation."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from scipy.stats import invgamma

from .bandit_algorithm import BanditAlgorithm
from .contextual_dataset import ContextualDataset
from .neural_bandit_model import NeuralBanditModel
import tensorflow as tf

import os
import pickle
import shutil


class NeuralLinearPosteriorSampling(BanditAlgorithm):
    """Full Bayesian linear regression on the last layer of a deep neural net."""

    def __init__(self, name, arguments, optimizer='RMS'):
        self.arguments = arguments
        self.arguments['optimizer'] = optimizer
        self.hparams = self.get_hparams()
        self.name = name
        self.latent_dim = self.hparams.layer_sizes[-1]
        self.num_actions = self.hparams.num_actions
        self.context_dim = self.hparams.context_dim
        self.initial_pulls = self.hparams.initial_pulls
        self.reset_lr = self.hparams.reset_lr
        
        self.master_params = dict()
        

        # Gaussian prior for each beta_i
        self._lambda_prior = self.hparams.lambda_prior

        self.mu = [
            np.zeros(self.latent_dim)
            for _ in range(self.hparams.num_actions)
        ]

        self.cov = [(1.0 / self.lambda_prior) * np.eye(self.latent_dim)
                    for _ in range(self.hparams.num_actions)]

        self.precision = [
            self.lambda_prior * np.eye(self.latent_dim)
            for _ in range(self.hparams.num_actions)
        ]

        # Inverse Gamma prior for each sigma2_i
        self._a0 = self.hparams.a0
        self._b0 = self.hparams.b0

        self.a = [self._a0 for _ in range(self.hparams.num_actions)]
        self.b = [self._b0 for _ in range(self.hparams.num_actions)]

        # Regression and NN Update Frequency
        self.update_freq_lr = self.hparams.training_freq
        self.update_freq_nn = self.hparams.training_freq_network

        self.t = 0
        self.optimizer_n = optimizer

        self.num_epochs = self.hparams.training_epochs
        
        memory_size = arguments['memory_size']
        self.data_h = ContextualDataset(
                            self.hparams.context_dim,
                            self.hparams.num_actions,
                            intercept=False,
                            memory_size=memory_size
        )
        self.latent_h = ContextualDataset(
                            self.latent_dim,
                            self.hparams.num_actions,
                            intercept=False,
                            memory_size=memory_size
        )

        self.bnn = NeuralBanditModel(optimizer, self.hparams, '{}-bnn'.format(name))

    def get_hparams(self):
        """converts arguments into hparams object."""
        arguments = self.arguments
        if arguments['activation'] == 'relu':
            activation_function = tf.nn.relu
        else:
            raise Exception("activation function not recognized: {}.".format(arguments.activation),
                            "Please pass string 'relu' (only supported option at this time.)")
        hparams = tf.contrib.training.HParams(
            num_actions=arguments['num_actions'],
            context_dim=arguments['context_dim'],
            init_scale=arguments['init_scale'],
            activation=activation_function,
            layer_sizes=arguments['layer_sizes'],
            batch_size=arguments['batch_size'],
            activate_decay=arguments['activate_decay'],
            initial_lr=arguments['initial_lr'],
            max_grad_norm=arguments['max_grad_norm'],
            show_training=arguments['show_training'],
            freq_summary=arguments['freq_summary'],
            buffer_s=arguments['buffer_s'],
            initial_pulls=arguments['initial_pulls'],
            reset_lr=arguments['reset_lr'],
            lr_decay_rate=arguments['lr_decay_rate'],
            training_freq=arguments['training_freq'],
            training_freq_network=arguments['training_freq_network'],
            training_epochs=arguments['training_epochs'],
            a0=arguments['a0'],
            b0=arguments['b0'],
            lambda_prior=arguments['lambda_prior']
        )
        return hparams    
    
    def get_representation(self, context):
        """
        Returns the latent feature vector from the neural network.
        This vector is called z in the Google Brain paper.
        """
        with self.bnn.graph.as_default():
            c = context.reshape((1, self.context_dim))
            z_context = self.bnn.sess.run(self.bnn.nn, feed_dict={self.bnn.x: c})
        return z_context
    
    def expected_values(self, context):
        """
        Computes expected values from context. Does not consider uncertainty.
        Args:
          context: Context for which the action need to be chosen.
        Returns:
          expected reward vector.
        """
        # Compute last-layer representation for the current context
        z_context = self.get_representation(context)
        
        # Compute sampled expected values, intercept is last component of beta
        vals = [
            np.dot(self.mu[i][:], z_context.T)
            for i in range(self.hparams.num_actions)
        ]
        return vals
        
    def _sample(self, context):
        # Sample sigma2, and beta conditional on sigma2
        sigma2_s = [
            self.b[i] * invgamma.rvs(self.a[i])
            for i in range(self.num_actions)
        ]

        try:
            beta_s = [
              np.random.multivariate_normal(self.mu[i], sigma2_s[i] * self.cov[i])
              for i in range(self.num_actions)
            ]
        except np.linalg.LinAlgError as e:
            # Sampling could fail if covariance is not positive definite
            print('Exception when sampling for {}.'.format(self.name))
            print('Details: {} | {}.'.format(e.message, e.args))
            d = self.latent_dim
            beta_s = [
              np.random.multivariate_normal(np.zeros((d)), np.eye(d))
              for i in range(self.num_actions)
            ]

        # Compute last-layer representation for the current context
        z_context = self.get_representation(context)

        # Apply Thompson Sampling to last-layer representation
        vals = [
            np.dot(beta_s[i], z_context.T) for i in range(self.num_actions)
        ]
        return vals
        
        
    def action(self, context):
        """Samples beta's from posterior, and chooses best action accordingly."""

        # Round robin until each action has been selected "initial_pulls" times
        if self.t < self.num_actions * self.initial_pulls:
            return self.t % self.num_actions
        else:
            vals = self._sample(context)
        return np.argmax(vals)

    def update(self, context, action, reward):
        """Updates the posterior using linear bayesian regression formula."""

        
        self.t += 1
        self.data_h.add(context, action, reward)
        c = context.reshape((1, self.context_dim))
        z_context = self.bnn.sess.run(self.bnn.nn, feed_dict={self.bnn.x: c})
        self.latent_h.add(z_context, action, reward)

        # Retrain the network on the original data (data_h)
        if self.t % self.update_freq_nn == 0:

            if self.reset_lr:
                self.bnn.assign_lr()
            self.bnn.train(self.data_h, self.num_epochs)

            # Update the latent representation of every datapoint collected so far
            new_z = self.bnn.sess.run(self.bnn.nn,
                                    feed_dict={self.bnn.x: self.data_h.contexts})
            self.latent_h.replace_data(contexts=new_z)

        # Update the Bayesian Linear Regression
        if self.t % self.update_freq_lr == 0:

            # Find all the actions to update
            actions_to_update = self.latent_h.actions[:-self.update_freq_lr]

        for action_v in np.unique(actions_to_update):

            # Update action posterior with formulas: \beta | z,y ~ N(mu_q, cov_q)
            z, y = self.latent_h.get_data(action_v)

            # The algorithm could be improved with sequential formulas (cheaper)
            s = np.dot(z.T, z)

            # Some terms are removed as we assume prior mu_0 = 0.
            precision_a = s + self.lambda_prior * np.eye(self.latent_dim)
            cov_a = np.linalg.inv(precision_a)
            mu_a = np.dot(cov_a, np.dot(z.T, y))

            # Inverse Gamma posterior update
            a_post = self.a0 + z.shape[0] / 2.0
            b_upd = 0.5 * np.dot(y.T, y)
            b_upd -= 0.5 * np.dot(mu_a.T, np.dot(precision_a, mu_a))
            b_post = self.b0 + b_upd

            # Store new posterior distributions
            self.mu[action_v] = mu_a
            self.cov[action_v] = cov_a
            self.precision[action_v] = precision_a
            self.a[action_v] = a_post
            self.b[action_v] = b_post
            
    def save(self, path):
        """saves model to path"""
        os.mkdir('tmp')
        bnn_temp = self.bnn
        self.bnn = None
        hparams_temp = self.hparams
        self.hparams = None
        pickle_path = os.path.join('tmp', 'master.pkl')
        with open(pickle_path, 'wb') as f:
            pickle.dump(self, f)
        self.bnn = bnn_temp
        weights_path = os.path.join('tmp', 'weights')
        with self.bnn.graph.as_default():
            init_op = tf.global_variables_initializer()
            sess = tf.Session()
            sess.run(init_op)
            saver = tf.train.Saver()
            saver.save(sess, weights_path)
        shutil.make_archive(path, 'zip', 'tmp')
        os.remove(pickle_path)
        os.remove(weights_path + '.data-00000-of-00001')
        os.remove(os.path.join('tmp', 'checkpoint'))
        os.remove(os.path.join('tmp', 'weights.meta'))
        os.remove(os.path.join('tmp', 'weights.index'))
        os.rmdir('tmp')
        self.hparams = hparams_temp

    @property
    def a0(self):
        return self._a0

    @property
    def b0(self):
        return self._b0

    @property
    def lambda_prior(self):
        return self._lambda_prior