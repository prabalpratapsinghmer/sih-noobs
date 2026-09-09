"""Feature Engineering Module for Cybercrime Prediction Framework.

Transforms raw synthetic data into model-ready features for:
- Spatio-Temporal Transformer (ATM prediction)
- Graph Neural Network (Mule detection)
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import yaml
from pathlib import Path
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import torch
from torch_geometric.data import Data


class FeatureEngineer:
    """Feature engineering for cybercrime prediction models."""

    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize feature engineer.

        Args:
            config_path: Path to configuration file
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.data_config = self.config['data']
        self.st_config = self.config['models']['spatio_temporal']
        self.gnn_config = self.config['models']['mule_detection']

        # Scalers and encoders
        self.spatial_scaler = StandardScaler()
        self.temporal_scaler = StandardScaler()
        self.label_encoders = {}
        self.fitted = False

    def load_raw_data(self, data_dir: str = 'data/raw') -> Dict[str, pd.DataFrame]:
        """Load raw data from CSV files.

        Args:
            data_dir: Directory containing raw data files

        Returns:
            Dictionary of raw DataFrames
        """
        data_path = Path(data_dir)
        return {
            'atms': pd.read_csv(data_path / 'atms.csv'),
            'mule_networks': pd.read_csv(data_path / 'mule_networks.csv'),
            'complaints': pd.read_csv(data_path / 'complaints.csv'),
            'transactions': pd.read_csv(data_path / 'transactions.csv')
        }

    def engineer_st_features(self, raw_data: Dict[str, pd.DataFrame]) -> Tuple[np.ndarray, np.ndarray]:
        """Engineer features for Spatio-Temporal Transformer.

        Creates features for ATM prediction:
        - Spatial features: lat, lon, metro_dist, police_dist, area_type, traffic, fraud_history
        - Temporal features: hour, day_of_week, is_weekend, is_night, time_since_complaint
        - Target: ATM ID (0-499)

        Args:
            raw_data: Dictionary of raw DataFrames

        Returns:
            Tuple of (features, targets)
        """
        atms = raw_data['atms'].copy()
        complaints = raw_data['complaints'].copy()
        transactions = raw_data['transactions'].copy()

        # Merge complaints with transactions (only completed withdrawals at ATMs)
        tx_atm = transactions[
            (transactions['transaction_type'] == 'withdrawal') &
            (transactions['status'] == 'completed')
        ].merge(atms[['atm_id', 'latitude', 'longitude', 'metro_distance', 'police_distance',
                      'area_type', 'traffic_density', 'fraud_history_count']],
                on='atm_id', how='left')

        # Merge with complaints to get fraud context
        df = tx_atm.merge(complaints[['complaint_id', 'fraud_date', 'fraud_amount', 'fraud_type',
                                       'victim_latitude', 'victim_longitude']],
                          on='complaint_id', how='left')

        # Parse datetime columns
        df['transaction_time'] = pd.to_datetime(df['transaction_time'])
        df['fraud_date'] = pd.to_datetime(df['fraud_date'])

        # Spatial features
        spatial_features = df[['latitude', 'longitude', 'metro_distance', 'police_distance',
                               'traffic_density', 'fraud_history_count']].values

        # Area type encoding
        if 'area_type_encoder' not in self.label_encoders:
            self.label_encoders['area_type_encoder'] = LabelEncoder()
            df['area_type_encoded'] = self.label_encoders['area_type_encoder'].fit_transform(df['area_type'])
        else:
            df['area_type_encoded'] = self.label_encoders['area_type_encoder'].transform(df['area_type'])

        spatial_features = np.hstack([spatial_features, df[['area_type_encoded']].values])

        # Temporal features
        df['hour_of_day'] = df['transaction_time'].dt.hour
        df['day_of_week'] = df['transaction_time'].dt.weekday
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        df['is_night'] = ((df['hour_of_day'] >= 2) & (df['hour_of_day'] <= 5)).astype(int)
        df['time_since_complaint'] = (df['transaction_time'] - df['fraud_date']).dt.total_seconds() / 3600

        # Cyclical encoding for hour and day
        df['hour_sin'] = np.sin(2 * np.pi * df['hour_of_day'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour_of_day'] / 24)
        df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)

        temporal_features = df[['hour_sin', 'hour_cos', 'day_sin', 'day_cos',
                                 'is_weekend', 'is_night', 'time_since_complaint']].values

        # Target: ATM index
        atm_to_idx = {atm_id: idx for idx, atm_id in enumerate(sorted(atms['atm_id'].unique()))}
        targets = df['atm_id'].map(atm_to_idx).values

        # Fit scalers if not already fitted
        if not self.fitted:
            self.spatial_scaler.fit(spatial_features)
            self.temporal_scaler.fit(temporal_features)
            self.fitted = True

        # Scale features
        spatial_features = self.spatial_scaler.transform(spatial_features)
        temporal_features = self.temporal_scaler.transform(temporal_features)

        # Combine features
        features = np.hstack([spatial_features, temporal_features])

        return features, targets

    def engineer_gnn_features(self, raw_data: Dict[str, pd.DataFrame]) -> Tuple[Data, np.ndarray]:
        """Engineer graph features for Mule Detection GNN.

        Creates transaction network graph where:
        - Nodes: Accounts (victim, suspect, intermediary)
        - Edges: Transactions between accounts
        - Node features: Transaction velocity, inflow/outflow, holding time, etc.
        - Labels: Whether account is a mule

        Args:
            raw_data: Dictionary of raw DataFrames

        Returns:
            Tuple of (PyG Data object, node labels)
        """
        transactions = raw_data['transactions'].copy()
        mule_networks = raw_data['mule_networks'].copy()

        # Build account transaction history
        all_accounts = set(transactions['from_account'].unique()) | set(transactions['to_account'].unique())
        account_to_idx = {acc: idx for idx, acc in enumerate(sorted(all_accounts))}

        # Create node features for each account
        num_accounts = len(account_to_idx)
        node_features = np.zeros((num_accounts, self.gnn_config['input_dim']))

        # Compute account-level features
        for account, idx in account_to_idx.items():
            # Outgoing transactions
            out_tx = transactions[transactions['from_account'] == account]
            # Incoming transactions
            in_tx = transactions[transactions['to_account'] == account]

            # Feature 0: Out-degree (number of outgoing transactions)
            node_features[idx, 0] = len(out_tx)

            # Feature 1: In-degree (number of incoming transactions)
            node_features[idx, 1] = len(in_tx)

            # Feature 2: Total outflow amount
            node_features[idx, 2] = out_tx['amount'].sum() if len(out_tx) > 0 else 0

            # Feature 3: Total inflow amount
            node_features[idx, 3] = in_tx['amount'].sum() if len(in_tx) > 0 else 0

            # Feature 4: Average holding time (time between incoming and outgoing)
            if len(in_tx) > 0 and len(out_tx) > 0:
                in_times = pd.to_datetime(in_tx['transaction_time']).values
                out_times = pd.to_datetime(out_tx['transaction_time']).values
                # Simple proxy: average time diff
                if len(in_times) > 0 and len(out_times) > 0:
                    min_diff = np.min(np.abs(out_times[:, None] - in_times[None, :])) / np.timedelta64(1, 'h')
                    node_features[idx, 4] = min_diff
                else:
                    node_features[idx, 4] = 0
            else:
                node_features[idx, 4] = 0

            # Feature 5: Transaction velocity (transactions per hour)
            all_tx = pd.concat([in_tx, out_tx])
            if len(all_tx) > 1:
                times = pd.to_datetime(all_tx['transaction_time']).sort_values()
                time_span = (times.iloc[-1] - times.iloc[0]).total_seconds() / 3600
                node_features[idx, 5] = len(all_tx) / max(time_span, 1)
            else:
                node_features[idx, 5] = 0

            # Feature 6: Suspicious timing ratio (2-5 AM transactions)
            all_tx_times = pd.to_datetime(all_tx['transaction_time'])
            night_tx = ((all_tx_times.dt.hour >= 2) & (all_tx_times.dt.hour <= 5)).sum()
            node_features[idx, 6] = night_tx / max(len(all_tx), 1)

            # Feature 7: Round amount pattern (amounts ending in 000, 500, etc.)
            round_amounts = (all_tx['amount'] % 1000 == 0).sum()
            node_features[idx, 7] = round_amounts / max(len(all_tx), 1)

            # Feature 8: Outflow/Inflow ratio
            if node_features[idx, 3] > 0:
                node_features[idx, 8] = node_features[idx, 2] / node_features[idx, 3]
            else:
                node_features[idx, 8] = 0

        # Build edges from transactions
        edges = []
        for _, tx in transactions.iterrows():
            from_idx = account_to_idx[tx['from_account']]
            to_idx = account_to_idx[tx['to_account']]
            edges.append([from_idx, to_idx])

        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous() if edges else torch.empty((2, 0), dtype=torch.long)

        # Create labels: mule accounts based on mule networks
        # For synthetic data, we'll use the mule flag from transactions
        mule_accounts = set()
        for _, tx in transactions[transactions['is_mule'] == True].iterrows():
            mule_accounts.add(tx['from_account'])
            mule_accounts.add(tx['to_account'])

        labels = np.zeros(num_accounts)
        for account, idx in account_to_idx.items():
            if account in mule_accounts:
                labels[idx] = 1

        # Create PyG Data object
        x = torch.tensor(node_features, dtype=torch.float)
        y = torch.tensor(labels, dtype=torch.float)
        data = Data(x=x, edge_index=edge_index, y=y)

        return data, labels

    def prepare_st_datasets(self, features: np.ndarray, targets: np.ndarray) -> Dict[str, Tuple]:
        """Prepare train/val/test splits for Spatio-Temporal model.

        Args:
            features: Combined feature array
            targets: Target array

        Returns:
            Dictionary with train/val/test splits
        """
        split_config = self.config['training']['spatio_temporal']['data_split']

        # First split: train vs (val + test)
        # Don't use stratify for multi-class with rare classes
        X_train, X_temp, y_train, y_temp = train_test_split(
            features, targets,
            test_size=(split_config['val'] + split_config['test']),
            random_state=split_config['random_seed']
        )

        # Second split: val vs test
        val_ratio = split_config['val'] / (split_config['val'] + split_config['test'])
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp,
            test_size=1 - val_ratio,
            random_state=split_config['random_seed']
        )

        return {
            'train': (X_train, y_train),
            'val': (X_val, y_val),
            'test': (X_test, y_test)
        }

    def save_processed_data(self, st_data: Dict, gnn_data: Data, output_dir: str = 'data/processed'):
        """Save processed features to disk.

        Args:
            st_data: Dictionary of ST model splits
            gnn_data: PyG Data object for GNN
            output_dir: Output directory
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save ST data
        for split_name, (X, y) in st_data.items():
            np.save(output_path / f'st_X_{split_name}.npy', X)
            np.save(output_path / f'st_y_{split_name}.npy', y)

        # Save GNN data
        torch.save(gnn_data, output_path / 'gnn_data.pt')

        # Save scalers and encoders
        import joblib
        joblib.dump(self.spatial_scaler, output_path / 'spatial_scaler.joblib')
        joblib.dump(self.temporal_scaler, output_path / 'temporal_scaler.joblib')
        joblib.dump(self.label_encoders, output_path / 'label_encoders.joblib')

        print(f"[OK] Saved processed data to {output_path}")

    def load_processed_data(self, input_dir: str = 'data/processed') -> Tuple[Dict, Data]:
        """Load processed features from disk.

        Args:
            input_dir: Input directory

        Returns:
            Tuple of (ST data dict, GNN Data object)
        """
        input_path = Path(input_dir)

        st_data = {}
        for split in ['train', 'val', 'test']:
            X = np.load(input_path / f'st_X_{split}.npy')
            y = np.load(input_path / f'st_y_{split}.npy')
            st_data[split] = (X, y)

        gnn_data = torch.load(input_path / 'gnn_data.pt', weights_only=False)

        return st_data, gnn_data


def main():
    """Main function to run feature engineering."""
    print("=" * 60)
    print("CYBERCRIME PREDICTION FRAMEWORK - FEATURE ENGINEERING")
    print("=" * 60)
    print()

    engineer = FeatureEngineer()

    # Load raw data
    print("Loading raw data...")
    raw_data = engineer.load_raw_data('data/raw')

    # Engineer ST features
    print("Engineering Spatio-Temporal features...")
    st_features, st_targets = engineer.engineer_st_features(raw_data)
    print(f"  Features shape: {st_features.shape}")
    print(f"  Targets shape: {st_targets.shape}")

    # Prepare ST datasets
    print("Preparing train/val/test splits...")
    st_data = engineer.prepare_st_datasets(st_features, st_targets)
    for split, (X, y) in st_data.items():
        print(f"  {split}: X={X.shape}, y={y.shape}")

    # Engineer GNN features
    print("Engineering GNN features...")
    gnn_data, gnn_labels = engineer.engineer_gnn_features(raw_data)
    print(f"  Nodes: {gnn_data.x.shape[0]}")
    print(f"  Edges: {gnn_data.edge_index.shape[1]}")
    print(f"  Node features: {gnn_data.x.shape[1]}")
    print(f"  Mule accounts: {int(gnn_labels.sum())} / {len(gnn_labels)}")

    # Save processed data
    print("Saving processed data...")
    engineer.save_processed_data(st_data, gnn_data)

    print()
    print("=" * 60)
    print("[SUCCESS] FEATURE ENGINEERING COMPLETED!")
    print("=" * 60)


if __name__ == '__main__':
    main()