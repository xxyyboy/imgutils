import torch
from torch import nn

from torch.nn import functional as F


class FocalLoss(nn.Module):
    """
    Based on https://discuss.pytorch.org/t/is-this-a-correct-implementation-for-focal-loss-in-pytorch/43327/8
    """

    def __init__(self, weight=None, gamma=2., reduction='mean'):
        nn.Module.__init__(self)
        weight = torch.as_tensor(weight).float() if weight is not None else weight
        self.register_buffer('weight', weight)

        self.gamma = gamma
        self.reduction = reduction

    def forward(self, input_tensor, target_tensor):
        log_prob = F.log_softmax(input_tensor, dim=-1)
        prob = torch.exp(log_prob)
        return F.nll_loss(
            ((1 - prob) ** self.gamma) * log_prob,
            target_tensor,
            weight=self.weight,
            reduction=self.reduction
        )


class NTXentLoss(nn.Module):
    """
    Inspired from https://blog.csdn.net/cziun/article/details/119118768 .
    """

    def __init__(self, tau: float = 1.0, eps: float = 1e-8):
        nn.Module.__init__(self)
        self.register_buffer('tau', torch.as_tensor(tau, dtype=torch.float))
        self.register_buffer('eps', torch.as_tensor(eps, dtype=torch.float))

    def forward(self, similarities, state):
        """
        :param similarities: Similarities, float32[N]
        :param state: Positive sample or not, bool[N]
        """
        negs = similarities[~state]
        pos_items = []
        for pos in similarities[state]:
            current_sims = torch.cat([pos.reshape(-1), negs])
            exp_sims = torch.exp(current_sims / self.tau)
            pos_items.append(-torch.log(exp_sims[0] / exp_sims.sum()))

        pos_tensor = torch.stack(pos_items)
        return (pos_tensor.sum() + self.eps) / (pos_tensor.shape[0] + self.eps)