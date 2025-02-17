from torch import nn


class Core:
    """
    Base class for the core models where shared features (across neurons) are computed.
    """

    def initialize(self):
        """
        Initialization applied on the core.
        """
        raise NotImplementedError("initialize method must be implemented by the inheriting class")

    def __repr__(self):
        s = super().__repr__()
        s += " [{} regularizers: ".format(self.__class__.__name__)
        ret = []
        for attr in filter(lambda x: "gamma" in x or "skip" in x, dir(self)):
            ret.append("{} = {}".format(attr, getattr(self, attr)))
        return s + "|".join(ret) + "]\n"


class Core2d(Core):
    """
    Base class for the core models, taking 2d inputs and computing nonlinear features.
    """

    def initialize(self):
        """
        Initialization applied on the core.
        """
        self.apply(self.init_conv)

    @staticmethod
    def init_conv(m):
        """
        Initialize convolution layers with:
            - weights: xavier_normal
            - biases: 0

        Args:
            m (nn.Module): a pytorch nn module.
        """
        if isinstance(m, nn.Conv2d):
            nn.init.xavier_normal_(m.weight.data)
            if m.bias is not None:
                m.bias.data.fill_(0)

    def forward(self, x):
        """
        Forward function for pytorch nn module.

        Args:
            x (torch.tensor): input of shape (batch, channels, height, width)
        """
        raise NotImplementedError("forward method must be implemented by the inheriting class")

    def regularizer(self):
        """
        Regularization applied on the core. Returns a scalar value.
        """
        raise NotImplementedError("regularizer method must be implemented by the inheriting class")
