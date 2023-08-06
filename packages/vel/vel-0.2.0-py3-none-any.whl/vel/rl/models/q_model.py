import gym

from vel.api.base import LinearBackboneModel, Model, ModelFactory
from vel.rl.modules.q_head import QHead


class QModel(Model):
    """ Wraps a backbone model into API we need for Deep Q-Learning """

    def __init__(self, backbone: LinearBackboneModel, action_space: gym.Space):
        super().__init__()

        self.backbone = backbone
        self.q_head = QHead(input_dim=backbone.output_dim, action_space=action_space)

    def forward(self, observations):
        """ Model forward pass """
        base_output = self.backbone(observations)
        q_values = self.q_head(base_output)
        return q_values

    def reset_weights(self):
        """ Initialize weights to reasonable defaults """
        self.backbone.reset_weights()
        self.q_head.reset_weights()

    def step(self, observations):
        """ Sample action from an action space for given state """
        q_values = self(observations)

        return {
            'actions': self.q_head.sample(q_values),
            'values': q_values
        }


class QModelFactory(ModelFactory):
    """ Factory class for q-learning models """
    def __init__(self, backbone: ModelFactory):
        self.backbone = backbone

    def instantiate(self, **extra_args):
        """ Instantiate the model """
        backbone = self.backbone.instantiate(**extra_args)
        return QModel(backbone, extra_args['action_space'])


def create(backbone: ModelFactory):
    """ Q-Learning model factory """
    return QModelFactory(backbone=backbone)
