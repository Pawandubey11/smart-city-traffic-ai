import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.train_sagemaker import train

def test_sagemaker_training():
    print("==================================================")
    print("PHASE 9 AWS SAGEMAKER TRAINING PIPELINE TEST")
    print("==================================================")
    
    test_model_dir = "models/weights_test"
    os.makedirs(test_model_dir, exist_ok=True)
    
    args = argparse.Namespace(
        epochs=1,
        batch_size=4,
        lr=0.001,
        sequence_length=16,
        num_gpus=0,
        model_dir=test_model_dir,
        output_data_dir="output_test"
    )
    
    train(args)
    
    weight_artifact = os.path.join(test_model_dir, "accident_cnn_lstm.pt")
    metrics_artifact = os.path.join(test_model_dir, "evaluation_metrics.json")
    
    assert os.path.exists(weight_artifact), f"Model weight artifact missing at {weight_artifact}"
    assert os.path.exists(metrics_artifact), f"Evaluation metrics missing at {metrics_artifact}"
    
    print(f"Verified SageMaker PyTorch Trained Model Artifact: {weight_artifact}")
    print(f"Verified Evaluation Metrics File: {metrics_artifact}")
    
    print("\n==================================================")
    print("PHASE 9 VERIFICATION COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_sagemaker_training()
