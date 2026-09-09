"""Data Synthesis Module for Cybercrime Prediction Framework.

Generates synthetic data for:
- ATM locations (500)
- Mule networks (50 networks)
- Complaints (5,000)
- Transactions (20,000)
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple
import yaml
from pathlib import Path


class DataSynthesizer:
    """Generate synthetic training data for the cybercrime prediction system."""

    def __init__(self, config_path: str = "config/config.yaml", seed: int = 42):
        """Initialize the data synthesizer.

        Args:
            config_path: Path to configuration file
            seed: Random seed for reproducibility
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.synthesis_config = self.config['data']['synthesis']
        self.seed = seed
        np.random.seed(seed)
        random.seed(seed)

        # Geographic bounds (Bangalore)
        self.lat_min = self.synthesis_config['bangalore']['lat_min']
        self.lat_max = self.synthesis_config['bangalore']['lat_max']
        self.lon_min = self.synthesis_config['bangalore']['lon_min']
        self.lon_max = self.synthesis_config['bangalore']['lon_max']

        # ATM data storage
        self.atms = []
        self.mule_networks = []
        self.complaints = []
        self.transactions = []

    def generate_all(self) -> Dict[str, pd.DataFrame]:
        """Generate all synthetic data.

        Returns:
            Dictionary containing all generated DataFrames
        """
        print("Starting data synthesis...")

        # Generate in order (transactions depend on complaints and ATMs)
        self._generate_atms()
        self._generate_mule_networks()
        self._generate_complaints()
        self._generate_transactions()

        # Convert to DataFrames
        data = {
            'atms': pd.DataFrame(self.atms),
            'mule_networks': pd.DataFrame(self.mule_networks),
            'complaints': pd.DataFrame(self.complaints),
            'transactions': pd.DataFrame(self.transactions)
        }

        print(f"[OK] Generated {len(self.atms)} ATMs")
        print(f"[OK] Generated {len(self.mule_networks)} mule networks")
        print(f"[OK] Generated {len(self.complaints)} complaints")
        print(f"[OK] Generated {len(self.transactions)} transactions")

        return data

    def _generate_atms(self):
        """Generate synthetic ATM locations."""
        num_atms = self.synthesis_config['num_atms']

        # Generate metro stations and police stations for proximity
        metro_stations = self._generate_metro_stations(20)
        police_stations = self._generate_police_stations(30)

        # Mark some ATMs as fraud hotspots
        hotspot_atms = random.sample(range(num_atms), self.synthesis_config['fraud']['hotspot_atms'])

        for atm_id in range(num_atms):
            lat = np.random.uniform(self.lat_min, self.lat_max)
            lon = np.random.uniform(self.lon_min, self.lon_max)

            # Calculate distances to nearest metro and police station
            metro_dist = self._min_distance(lat, lon, metro_stations)
            police_dist = self._min_distance(lat, lon, police_stations)

            # Determine area type
            area_type = random.choice(['urban', 'suburban', 'commercial', 'residential'])

            # Traffic density (0-1 scale)
            traffic_density = np.random.beta(2, 2)  # Centered around 0.5

            # Fraud history (higher for hotspot ATMs)
            fraud_history = np.random.exponential(2) if atm_id in hotspot_atms else np.random.exponential(0.5)

            atm = {
                'atm_id': f'ATM_{atm_id:04d}',
                'latitude': lat,
                'longitude': lon,
                'area_type': area_type,
                'metro_distance': metro_dist,
                'police_distance': police_dist,
                'traffic_density': traffic_density,
                'fraud_history_count': int(fraud_history),
                'is_hotspot': atm_id in hotspot_atms,
                'bank_name': random.choice(['SBI', 'HDFC', 'ICICI', 'Axis', 'PNB', 'BOB']),
                'atm_type': random.choice(['on-site', 'off-site', 'mobile']),
                '24x7': random.choice([True, False]),
                'cash_capacity': random.choice([500000, 1000000, 2000000]),
                'created_at': datetime.now() - timedelta(days=random.randint(365, 1825))
            }
            self.atms.append(atm)

    def _generate_metro_stations(self, num_stations: int) -> List[Tuple[float, float]]:
        """Generate metro station locations."""
        stations = []
        for _ in range(num_stations):
            lat = np.random.uniform(self.lat_min, self.lat_max)
            lon = np.random.uniform(self.lon_min, self.lon_max)
            stations.append((lat, lon))
        return stations

    def _generate_police_stations(self, num_stations: int) -> List[Tuple[float, float]]:
        """Generate police station locations."""
        stations = []
        for _ in range(num_stations):
            lat = np.random.uniform(self.lat_min, self.lat_max)
            lon = np.random.uniform(self.lon_min, self.lon_max)
            stations.append((lat, lon))
        return stations

    def _min_distance(self, lat: float, lon: float, points: List[Tuple[float, float]]) -> float:
        """Calculate minimum distance from a point to a set of points (in km)."""
        min_dist = float('inf')
        for p_lat, p_lon in points:
            dist = self._haversine_distance(lat, lon, p_lat, p_lon)
            min_dist = min(min_dist, dist)
        return min_dist

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two GPS coordinates using Haversine formula."""
        R = 6371  # Earth's radius in km

        lat1_rad = np.radians(lat1)
        lat2_rad = np.radians(lat2)
        delta_lat = np.radians(lat2 - lat1)
        delta_lon = np.radians(lon2 - lon1)

        a = np.sin(delta_lat / 2) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(delta_lon / 2) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        return R * c

    def _generate_mule_networks(self):
        """Generate synthetic mule account networks."""
        num_networks = self.synthesis_config['num_mule_networks']

        for network_id in range(num_networks):
            # Each network has 5-20 mule accounts
            num_mules = random.randint(5, 20)

            # Network characteristics
            sophistication = random.choice(['low', 'medium', 'high'])
            activity_period = random.randint(30, 365)  # days

            network = {
                'network_id': f'NET_{network_id:04d}',
                'num_mules': num_mules,
                'sophistication': sophistication,
                'activity_period_days': activity_period,
                'total_fraud_amount': random.randint(100000, 10000000),
                'detection_status': random.choice(['active', 'detected', 'dormant']),
                'created_at': datetime.now() - timedelta(days=random.randint(30, 365))
            }
            self.mule_networks.append(network)

    def _generate_complaints(self):
        """Generate synthetic cybercrime complaints."""
        num_complaints = self.synthesis_config['num_complaints']

        fraud_types = [
            'phishing', 'online_fraud', 'investment_scam', 'job_scam',
            'loan_fraud', 'romance_scam', 'lottery_scam', 'insurance_fraud'
        ]

        for complaint_id in range(num_complaints):
            # Complaint timing
            report_date = datetime.now() - timedelta(days=random.randint(1, 365))
            fraud_date = report_date - timedelta(hours=random.randint(1, 72))

            # Fraud amount
            fraud_amount = random.randint(5000, 500000)

            # Victim account
            victim_account = f'VICT_{random.randint(100000, 999999)}'

            # Suspect account (may be linked to mule network)
            suspect_account = f'SUSP_{random.randint(100000, 999999)}'

            # Geographic info
            victim_lat = np.random.uniform(self.lat_min, self.lat_max)
            victim_lon = np.random.uniform(self.lon_min, self.lon_max)

            complaint = {
                'complaint_id': f'COMP_{complaint_id:06d}',
                'fraud_type': random.choice(fraud_types),
                'fraud_amount': fraud_amount,
                'fraud_date': fraud_date,
                'report_date': report_date,
                'victim_account': victim_account,
                'suspect_account': suspect_account,
                'victim_latitude': victim_lat,
                'victim_longitude': victim_lon,
                'status': random.choice(['pending', 'investigating', 'resolved', 'closed']),
                'priority': random.choice(['low', 'medium', 'high', 'critical']),
                'assigned_officer': f'OFF_{random.randint(100, 999)}',
                'description': f'Cybercrime complaint {complaint_id}',
                'created_at': report_date
            }
            self.complaints.append(complaint)

    def _generate_transactions(self):
        """Generate synthetic transaction data."""
        num_transactions = self.synthesis_config['num_transactions']

        for tx_id in range(num_transactions):
            # Get associated complaint and ATM
            complaint = random.choice(self.complaints)
            atm = random.choice(self.atms)

            # Transaction timing (within 6 hours of fraud)
            tx_time = complaint['fraud_date'] + timedelta(hours=random.uniform(0, 6))

            # Transaction amount (fraction of fraud amount)
            tx_amount = complaint['fraud_amount'] * random.uniform(0.1, 1.0)

            # Determine if this is a mule transaction
            is_mule = random.random() < 0.2  # 20% are mule transactions

            # Transaction features
            hour_of_day = tx_time.hour
            day_of_week = tx_time.weekday()
            is_weekend = day_of_week >= 5
            is_night = 2 <= hour_of_day <= 5

            transaction = {
                'transaction_id': f'TXN_{tx_id:07d}',
                'complaint_id': complaint['complaint_id'],
                'atm_id': atm['atm_id'],
                'from_account': complaint['suspect_account'],
                'to_account': f'ACC_{random.randint(100000, 999999)}',
                'amount': tx_amount,
                'transaction_time': tx_time,
                'hour_of_day': hour_of_day,
                'day_of_week': day_of_week,
                'is_weekend': is_weekend,
                'is_night': is_night,
                'is_mule': is_mule,
                'transaction_type': random.choice(['withdrawal', 'transfer', 'deposit']),
                'status': random.choice(['completed', 'pending', 'failed']),
                'created_at': tx_time
            }
            self.transactions.append(transaction)

    def save_data(self, data: Dict[str, pd.DataFrame], output_dir: str = 'data/raw'):
        """Save generated data to CSV files.

        Args:
            data: Dictionary of DataFrames to save
            output_dir: Output directory path
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for name, df in data.items():
            file_path = output_path / f'{name}.csv'
            df.to_csv(file_path, index=False)
            print(f"[OK] Saved {name} to {file_path}")

    def generate_validation_data(self) -> Dict[str, pd.DataFrame]:
        """Generate validation/test dataset.

        Returns:
            Dictionary containing validation DataFrames
        """
        print("\nGenerating validation data...")

        # Use different seed for validation data
        np.random.seed(self.seed + 1000)
        random.seed(self.seed + 1000)

        # Generate smaller dataset for validation
        original_config = self.synthesis_config.copy()
        self.synthesis_config['num_atms'] = 50
        self.synthesis_config['num_mule_networks'] = 5
        self.synthesis_config['num_complaints'] = 500
        self.synthesis_config['num_transactions'] = 2000
        self.synthesis_config['fraud']['hotspot_atms'] = 10  # Adjust for smaller dataset

        # Reset data
        self.atms = []
        self.mule_networks = []
        self.complaints = []
        self.transactions = []

        validation_data = self.generate_all()

        # Restore original config
        self.synthesis_config = original_config

        return validation_data


def main():
    """Main function to run data synthesis."""
    import argparse

    parser = argparse.ArgumentParser(description='Synthesize cybercrime data')
    parser.add_argument('--config', default='config/config.yaml', help='Config file path')
    parser.add_argument('--output', default='data/raw', help='Output directory')
    parser.add_argument('--validation', action='store_true', help='Generate validation data')

    args = parser.parse_args()

    synthesizer = DataSynthesizer(config_path=args.config)

    # Generate training data
    train_data = synthesizer.generate_all()
    synthesizer.save_data(train_data, args.output)

    # Generate validation data if requested
    if args.validation:
        val_data = synthesizer.generate_validation_data()
        synthesizer.save_data(val_data, 'data/validation')

    print("\n[OK] Data synthesis completed successfully!")


if __name__ == '__main__':
    main()
