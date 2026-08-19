import os
import sys
import json
import argparse
import logging
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

# Add current working directory and project root to sys.path
cwd = os.getcwd()
sys.path.insert(0, cwd)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

try:
    from models.cnn_lstm.accident_net import SpatialTemporalAccidentNet
except ImportError:
    from cnn_lstm.accident_net import SpatialTemporalAccidentNet

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("SageMakerTrainer")

def generate_synthetic_training_data(num_samples: int = 40, seq_len: int = 16):
    """Generates synthetic sequence tensors for SageMaker model training verification."""
    logger.info(f"Generating synthetic training dataset: {num_samples} sequences of length {seq_len}")
    
    # Half non-accident, half accident sequence tensors
    X_list = []
    y_list = []
    
    for i in range(num_samples):
        # Shape: (16, 3, 224, 224)
        seq = np.random.randn(seq_len, 3, 224, 224).astype(np.float32)
        label = 1.0 if i >= (num_samples // 2) else 0.0
        
        if label == 1.0:
            # Inject simulated high visual intensity motion in last 4 frames
            seq[-4:] += 2.5
            
        X_list.append(seq)
        y_list.append([label])
        
    X_tensor = torch.tensor(np.array(X_list), dtype=torch.float32)
    y_tensor = torch.tensor(np.array(y_list), dtype=torch.float32)
    
    return TensorDataset(X_tensor, y_tensor)

def train(args):
    """SageMaker Training Execution Loop."""
    logger.info("==================================================")
    logger.info("STARTING AWS SAGEMAKER CNN-LSTM MODEL TRAINING")
    logger.info(f"Hyperparameters - Epochs: {args.epochs}, Batch Size: {args.batch_size}, LR: {args.lr}")
    logger.info("==================================================")
    
    device = torch.device("cuda" if torch.cuda.is_available() and args.num_gpus > 0 else "cpu")
    logger.info(f"Training on device: {device}")

    # 1. Dataset & DataLoader
    dataset = generate_synthetic_training_data(num_samples=40, seq_len=args.sequence_length)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)

    # 2. Model Initialization
    model = SpatialTemporalAccidentNet()
    model.to(device)

    # 3. Loss & Optimizer
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    # 4. Training Loop
    for epoch in range(1, args.epochs + 1):
        model.train()
        train_loss = 0.0
        
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item() * batch_x.size(0)

        train_loss = train_loss / train_size
        
        # Validation Evaluation
        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                batch_x, batch_y = batch_x.to(device), batch_y.to(device)
                outputs = model(batch_x)
                loss = criterion(outputs, batch_y)
                val_loss += loss.item() * batch_x.size(0)
                
                preds = (outputs >= 0.5).float()
                correct += (preds == batch_y).sum().item()
                total += batch_y.size(0)

        val_loss = val_loss / val_size if val_size > 0 else 0.0
        val_acc = (correct / total) if total > 0 else 1.0
        
        logger.info(f"Epoch [{epoch:02d}/{args.epochs:02d}] - Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f} | Val Acc: {val_acc*100:.1f}%")

    # 5. Export Trained Model Artifact
    os.makedirs(args.model_dir, exist_ok=True)
    model_save_path = os.path.join(args.model_dir, "accident_cnn_lstm.pt")
    torch.save(model.state_dict(), model_save_path)
    logger.info(f"Saved trained PyTorch model weights artifact to: {model_save_path}")
    
    # Save training metrics metadata
    metrics_path = os.path.join(args.model_dir, "evaluation_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump({"final_val_loss": val_loss, "final_val_acc": val_acc, "epochs": args.epochs}, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SageMaker PyTorch Accident Detection Model Trainer")
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--sequence-length", type=int, default=16)
    parser.add_argument("--num-gpus", type=int, default=0)
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR", "models/weights"))
    parser.add_argument("--output-data-dir", type=str, default=os.environ.get("SM_OUTPUT_DATA_DIR", "output"))
    
    args = parser.parse_args()
    train(args)
