import torch
import torch.nn as nn
import torchvision.models as models
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("AccidentCNN-LSTM")

class SpatialTemporalAccidentNet(nn.Module):
    """
    CNN + LSTM Architecture for Temporal Accident Detection.
    - CNN Backbone (ResNet18): Extracts spatial visual features per frame (512-dim).
    - LSTM Layer: Captures temporal movement dynamics across a 16-frame sequence window.
    - Classifier: Fully connected layer returning continuous accident probability (0.0 to 1.0).
    """
    def __init__(self, cnn_embed_dim: int = 512, lstm_hidden_dim: int = 256, num_layers: int = 2):
        super(SpatialTemporalAccidentNet, self).__init__()
        
        # 1. Spatial Feature Extractor (CNN)
        resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT if hasattr(models, 'ResNet18_Weights') else None)
        # Remove original classification fc layer
        self.cnn_backbone = nn.Sequential(*list(resnet.children())[:-1])
        self.cnn_fc = nn.Linear(resnet.fc.in_features, cnn_embed_dim)
        self.relu = nn.ReLU()
        
        # 2. Temporal Sequence Processor (LSTM)
        self.lstm = nn.LSTM(
            input_size=cnn_embed_dim,
            hidden_size=lstm_hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2 if num_layers > 1 else 0.0
        )
        
        # 3. Binary Classification Head
        self.classifier = nn.Sequential(
            nn.Linear(lstm_hidden_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward_single_frame(self, frame_tensor: torch.Tensor) -> torch.Tensor:
        """
        Extracts spatial feature vector for a single frame.
        Input: (B, 3, H, W)
        Output: (B, 512)
        """
        feats = self.cnn_backbone(frame_tensor) # (B, 512, 1, 1)
        feats = torch.flatten(feats, 1)        # (B, 512)
        embeds = self.relu(self.cnn_fc(feats))  # (B, 512)
        return embeds

    def forward(self, sequence_tensor: torch.Tensor) -> torch.Tensor:
        """
        Input: (Batch_Size, Sequence_Length, Channels, Height, Width) -> e.g. (B, 16, 3, 224, 224)
        Output: (Batch_Size, 1) -> Accident probabilities
        """
        b_size, seq_len, c, h, w = sequence_tensor.shape
        
        # Reshape to process all frames through CNN in parallel
        frames_flat = sequence_tensor.view(b_size * seq_len, c, h, w)
        frame_embeds_flat = self.forward_single_frame(frames_flat) # (B*16, 512)
        
        # Reshape back to sequence format for LSTM
        seq_embeds = frame_embeds_flat.view(b_size, seq_len, -1)  # (B, 16, 512)
        
        # Pass sequence through LSTM
        lstm_out, (h_n, c_n) = self.lstm(seq_embeds)               # (B, 16, lstm_hidden_dim)
        
        # Use final time step hidden representation
        final_seq_representation = lstm_out[:, -1, :]             # (B, lstm_hidden_dim)
        
        # Predict accident probability
        probs = self.classifier(final_seq_representation)          # (B, 1)
        return probs
