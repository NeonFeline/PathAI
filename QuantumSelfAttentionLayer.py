import torch
import torch.nn as nn
from qailab.torch import orca_layer

class QuantumSelfAttentionLayer(nn.Module):
    def __init__(self, classical_input_size, orca_in_features, orca_out_features):
        super(QuantumSelfAttentionLayer, self).__init__()
        

        self.keyMatrix = nn.Linear(classical_input_size, orca_in_features)
        self.queryMatrix = nn.Linear(classical_input_size, orca_in_features)
        self.valueMatrix = nn.Linear(classical_input_size, orca_out_features) 

        
        
        # ORCA quantum layer
        self.orca_layer = orca_layer.ORCALayer(
            in_features=orca_in_features,
            observable='avg-photons',
            gradient_mode='parameter-shift',
            n_samples=100,
            n_loops=2,
        )
        
        # Initialize a parameter buffer to store original key gradients
        self.register_buffer('orig_query', None)
        self.query_requires_grad = False
    
    def forward(self, x):
        # Save the original key tensor and its requires_grad state
        key = self.keyMatrix(x)
        query = self.queryMatrix(x)
        value = self.valueMatrix(x)
        
        self.orig_query = query
        self.query_requires_grad = query.requires_grad
        
        # Update ORCA parameters with the key
        self.orca_layer.set_thetas(query)
        
        # Register a hook for backward to capture gradients
        if self.query_requires_grad:
            # Get the parameter that was set in the ORCA layer
            for param in self.orca_layer.parameters():
                if param.shape == query.shape:
                    param.register_hook(lambda grad: self._save_grad_to_query(grad))
        
        # Process through quantum layer
        key_querry = self.orca_layer(key)

        output = key_querry * value
        
        return output
    
    def _save_grad_to_query(self, grad):
        # This function will be called during backward pass
        # It passes the gradient from the ORCA parameters back to the original key
        if self.orig_query.grad is None:
            self.orig_query.grad = grad.clone()
        else:
            self.orig_query.grad += grad.clone()
        return grad