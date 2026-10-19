"""Checkpoint-compatible architecture copied from the published DNN."""
import hashlib
import torch
from torch import nn

class DNN(nn.Module):
    def __init__(self, input_size=7, shared_layer_sizes=(256, 128),
                 output_layer_size=1, specific_layer_size=48):
        super().__init__()
        widths = [input_size, *shared_layer_sizes]
        self.shared_layers = nn.ModuleList([
            nn.Linear(a, b) for a, b in zip(widths[:-1], widths[1:])])
        self.output_layer = nn.Sequential(
            nn.Linear(widths[-1], specific_layer_size), nn.ReLU(),
            nn.Linear(specific_layer_size, output_layer_size))

    def forward(self, x):
        for layer in self.shared_layers:
            x = torch.relu(layer(x))
        return torch.sigmoid(self.output_layer(x))

def load_pretrained(model, path):
    if not path.is_file():
        raise FileNotFoundError(path)
    state = torch.load(path, map_location='cpu', weights_only=True)
    expected = model.state_dict()
    if set(state) != set(expected):
        raise ValueError('Checkpoint parameter names differ')
    for name, value in state.items():
        if value.shape != expected[name].shape or not torch.isfinite(value).all():
            raise ValueError(f'Invalid checkpoint tensor: {name}')
    if state['shared_layers.0.weight'].shape[1] != 7:
        raise ValueError('Expected seven inputs')
    model.load_state_dict(state, strict=True)
    assert all(torch.equal(model.state_dict()[k], v) for k, v in state.items())
    return {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'strict_loading': True, 'shapes': {k: list(v.shape) for k,v in state.items()}}

def freeze_shared(model):
    for param in model.shared_layers.parameters():
        param.requires_grad = False
    assert all(not p.requires_grad for p in model.shared_layers.parameters())
    assert all(p.requires_grad for p in model.output_layer.parameters())
    return {label: sum(p.numel() for p in model.parameters() if p.requires_grad == flag)
            for label,flag in [('frozen',False),('trainable',True)]}
