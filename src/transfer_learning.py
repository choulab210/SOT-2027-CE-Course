"""Fixed CPU training: no tuning, test-based selection, or source retraining."""
import random
import numpy as np
import torch
from torch import nn

def seed_everything(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)

def fit_network(model, x, y, epochs=50, batch_size=22, lr=0.01, norm_penalty=0.001):
    # For TL this is exactly Adam(model.output_layer.parameters(), lr=0.01).
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.Adam(params, lr=lr)
    assert {id(p) for g in optimizer.param_groups for p in g['params']} == {id(p) for p in params}
    before = {k:v.clone() for k,v in model.state_dict().items()}
    frozen = {k for k,p in model.named_parameters() if not p.requires_grad}
    x = torch.tensor(np.asarray(x), dtype=torch.float32)
    y = torch.tensor(np.asarray(y), dtype=torch.float32).reshape(-1,1)
    generator = torch.Generator().manual_seed(42)
    history = []
    model.train()
    for epoch in range(epochs):
        order = torch.randperm(len(x), generator=generator)
        total = 0.0
        for indices in order.split(batch_size):
            optimizer.zero_grad()                 # Clear previous gradients.
            probabilities = model(x[indices])      # Forward pass; original sigmoid.
            loss = nn.functional.binary_cross_entropy(probabilities, y[indices])
            # Original sum of tensor L2 norms (NOT squared-weight decay).
            loss = loss + norm_penalty * sum(p.norm(2) for p in model.parameters())
            loss.backward()                       # Compute gradients.
            optimizer.step()                      # Update trainable weights only.
            total += loss.item()*len(indices)
        history.append({'epoch':epoch+1,'loss_with_penalty':total/len(x)})
    after = model.state_dict()
    assert all(torch.equal(before[k], after[k]) for k in frozen)
    changed = [k for k in after if not torch.equal(before[k],after[k])]
    assert any(k.startswith('output_layer.') for k in changed)
    model.eval()
    return history, {'frozen_unchanged':True, 'changed_parameters':changed,
                     'optimizer_only_trainable':True}

def predict(model, x):
    model.eval()
    with torch.no_grad():
        p = model(torch.tensor(np.asarray(x), dtype=torch.float32)).numpy().ravel()
    if not np.isfinite(p).all(): raise ValueError('Nonfinite predictions')
    return p
