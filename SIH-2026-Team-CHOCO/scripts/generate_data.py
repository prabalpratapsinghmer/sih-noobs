"""Script to generate synthetic data for cybercrime prediction."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from models.utils.data_synthesis import DataSynthesizer


def main():
    """Generate synthetic training and validation data."""
    print("=" * 60)
    print("CYBERCRIME PREDICTION FRAMEWORK - DATA SYNTHESIS")
    print("=" * 60)
    print()

    # Initialize synthesizer
    synthesizer = DataSynthesizer(config_path='config/config.yaml')

    # Generate training data
    print("Generating TRAINING data...")
    train_data = synthesizer.generate_all()
    synthesizer.save_data(train_data, 'data/raw')

    print()

    # Generate validation data
    print("Generating VALIDATION data...")
    val_data = synthesizer.generate_validation_data()
    synthesizer.save_data(val_data, 'data/validation')

    print()
    print("=" * 60)
    print("[SUCCESS] DATA SYNTHESIS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print()

    # Print summary statistics
    print("SUMMARY STATISTICS:")
    print("-" * 60)
    print(f"Training Data:")
    print(f"  ATMs:           {len(train_data['atms'])}")
    print(f"  Mule Networks:  {len(train_data['mule_networks'])}")
    print(f"  Complaints:     {len(train_data['complaints'])}")
    print(f"  Transactions:   {len(train_data['transactions'])}")
    print()
    print(f"Validation Data:")
    print(f"  ATMs:           {len(val_data['atms'])}")
    print(f"  Mule Networks:  {len(val_data['mule_networks'])}")
    print(f"  Complaints:     {len(val_data['complaints'])}")
    print(f"  Transactions:   {len(val_data['transactions'])}")
    print("-" * 60)


if __name__ == '__main__':
    main()
