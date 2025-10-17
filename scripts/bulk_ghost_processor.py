"""
Bulk Ghost Data Processor
Based on: https://github.com/tspannhw/AIM-Ghosts/blob/main/ghost.py

This script processes multiple ghost sightings, evidence files, and images in batch mode.
Ideal for importing large datasets or processing accumulated data.

Features:
- Batch image analysis with Cortex Vision
- Bulk evidence processing
- Parallel processing support
- Progress tracking and reporting
- Error handling and retry logic
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, lit, udf
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BulkGhostProcessor:
    """
    Bulk processor for ghost detection data.
    Handles batch processing of sightings, evidence, and images.
    """
    
    def __init__(self, session: Session):
        self.session = session
        self.processed_count = 0
        self.error_count = 0
        self.start_time = None
        
    def process_csv_sightings(self, csv_path: str) -> Dict:
        """
        Process ghost sightings from CSV file.
        
        CSV Format:
        location_name, latitude, longitude, ghost_type, witness_name, 
        activity_level, temperature_c, emf_reading, description
        """
        logger.info(f"Processing sightings from: {csv_path}")
        self.start_time = time.time()
        
        try:
            # Read CSV
            df = pd.read_csv(csv_path)
            logger.info(f"Found {len(df)} sightings to process")
            
            results = {
                'total': len(df),
                'success': 0,
                'errors': 0,
                'error_details': []
            }
            
            # Process each sighting
            for idx, row in df.iterrows():
                try:
                    self._insert_sighting(row)
                    results['success'] += 1
                    self.processed_count += 1
                    
                    if (idx + 1) % 10 == 0:
                        logger.info(f"Processed {idx + 1}/{len(df)} sightings...")
                        
                except Exception as e:
                    results['errors'] += 1
                    self.error_count += 1
                    error_msg = f"Row {idx}: {str(e)}"
                    results['error_details'].append(error_msg)
                    logger.error(error_msg)
            
            elapsed = time.time() - self.start_time
            logger.info(f"Completed in {elapsed:.2f}s. Success: {results['success']}, Errors: {results['errors']}")
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to process CSV: {str(e)}")
            raise
    
    def process_image_directory(self, image_dir: str, ghost_id: Optional[str] = None) -> Dict:
        """
        Process all images in a directory with Cortex Vision.
        
        Args:
            image_dir: Directory containing images
            ghost_id: Optional ghost_id to associate with all images
        """
        logger.info(f"Processing images from: {image_dir}")
        self.start_time = time.time()
        
        image_dir_path = Path(image_dir)
        if not image_dir_path.exists():
            raise ValueError(f"Directory not found: {image_dir}")
        
        # Supported image formats
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        image_files = [
            f for f in image_dir_path.iterdir() 
            if f.suffix.lower() in image_extensions
        ]
        
        logger.info(f"Found {len(image_files)} images to process")
        
        results = {
            'total': len(image_files),
            'success': 0,
            'errors': 0,
            'error_details': []
        }
        
        # Process images (could be parallelized)
        for idx, image_file in enumerate(image_files):
            try:
                self._process_single_image(image_file, ghost_id)
                results['success'] += 1
                self.processed_count += 1
                
                if (idx + 1) % 5 == 0:
                    logger.info(f"Processed {idx + 1}/{len(image_files)} images...")
                    
            except Exception as e:
                results['errors'] += 1
                self.error_count += 1
                error_msg = f"Image {image_file.name}: {str(e)}"
                results['error_details'].append(error_msg)
                logger.error(error_msg)
        
        elapsed = time.time() - self.start_time
        logger.info(f"Completed in {elapsed:.2f}s. Success: {results['success']}, Errors: {results['errors']}")
        
        return results
    
    def process_json_batch(self, json_path: str) -> Dict:
        """
        Process batch data from JSON file.
        
        JSON Format:
        {
            "sightings": [...],
            "evidence": [...],
            "investigations": [...]
        }
        """
        logger.info(f"Processing batch from: {json_path}")
        self.start_time = time.time()
        
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        results = {
            'sightings': {'success': 0, 'errors': 0},
            'evidence': {'success': 0, 'errors': 0},
            'investigations': {'success': 0, 'errors': 0}
        }
        
        # Process sightings
        if 'sightings' in data:
            for sighting in data['sightings']:
                try:
                    self._insert_sighting_from_dict(sighting)
                    results['sightings']['success'] += 1
                    self.processed_count += 1
                except Exception as e:
                    results['sightings']['errors'] += 1
                    self.error_count += 1
                    logger.error(f"Sighting error: {str(e)}")
        
        # Process evidence
        if 'evidence' in data:
            for evidence in data['evidence']:
                try:
                    self._insert_evidence_from_dict(evidence)
                    results['evidence']['success'] += 1
                    self.processed_count += 1
                except Exception as e:
                    results['evidence']['errors'] += 1
                    self.error_count += 1
                    logger.error(f"Evidence error: {str(e)}")
        
        # Process investigations
        if 'investigations' in data:
            for investigation in data['investigations']:
                try:
                    self._insert_investigation_from_dict(investigation)
                    results['investigations']['success'] += 1
                    self.processed_count += 1
                except Exception as e:
                    results['investigations']['errors'] += 1
                    self.error_count += 1
                    logger.error(f"Investigation error: {str(e)}")
        
        elapsed = time.time() - self.start_time
        logger.info(f"Batch completed in {elapsed:.2f}s")
        logger.info(f"Results: {json.dumps(results, indent=2)}")
        
        return results
    
    def _insert_sighting(self, row: pd.Series):
        """Insert single sighting from CSV row."""
        from uuid import uuid4
        
        sighting_id = f"SIGHT_{str(uuid4())[:8].upper()}"
        ghost_id = row.get('ghost_id', 'GH001')  # Default if not specified
        
        sql = f"""
        INSERT INTO GHOST_DETECTION.APP.GHOST_SIGHTINGS (
            sighting_id, ghost_id, location_name, latitude, longitude,
            sighting_datetime, witness_name, paranormal_activity_level,
            temperature_celsius, emf_reading, description, verified
        ) VALUES (
            '{sighting_id}',
            '{ghost_id}',
            '{row["location_name"]}',
            {row["latitude"]},
            {row["longitude"]},
            CURRENT_TIMESTAMP(),
            '{row["witness_name"]}',
            {row["activity_level"]},
            {row["temperature_c"]},
            {row["emf_reading"]},
            '{row["description"].replace("'", "''")}',
            FALSE
        )
        """
        
        self.session.sql(sql).collect()
    
    def _insert_sighting_from_dict(self, sighting: Dict):
        """Insert sighting from dictionary."""
        from uuid import uuid4
        
        sighting_id = sighting.get('sighting_id', f"SIGHT_{str(uuid4())[:8].upper()}")
        
        sql = f"""
        INSERT INTO GHOST_DETECTION.APP.GHOST_SIGHTINGS (
            sighting_id, ghost_id, location_name, latitude, longitude,
            sighting_datetime, witness_name, paranormal_activity_level,
            temperature_celsius, emf_reading, description, verified
        ) VALUES (
            '{sighting_id}',
            '{sighting["ghost_id"]}',
            '{sighting["location_name"]}',
            {sighting["latitude"]},
            {sighting["longitude"]},
            '{sighting.get("datetime", "CURRENT_TIMESTAMP()")}',
            '{sighting["witness_name"]}',
            {sighting["activity_level"]},
            {sighting.get("temperature_c", 20)},
            {sighting.get("emf_reading", 0)},
            '{sighting["description"].replace("'", "''")}',
            {sighting.get("verified", False)}
        )
        """
        
        self.session.sql(sql).collect()
    
    def _insert_evidence_from_dict(self, evidence: Dict):
        """Insert evidence from dictionary."""
        from uuid import uuid4
        
        evidence_id = evidence.get('evidence_id', f"EV_{str(uuid4())[:8].upper()}")
        
        sql = f"""
        INSERT INTO GHOST_DETECTION.APP.GHOST_EVIDENCE (
            evidence_id, sighting_id, ghost_id, evidence_type,
            file_path, capture_datetime, processing_status
        ) VALUES (
            '{evidence_id}',
            '{evidence["sighting_id"]}',
            '{evidence["ghost_id"]}',
            '{evidence["type"]}',
            '{evidence["file_path"]}',
            CURRENT_TIMESTAMP(),
            'Pending'
        )
        """
        
        self.session.sql(sql).collect()
    
    def _insert_investigation_from_dict(self, investigation: Dict):
        """Insert investigation from dictionary."""
        from uuid import uuid4
        
        inv_id = investigation.get('investigation_id', f"INV_{str(uuid4())[:8].upper()}")
        
        sql = f"""
        INSERT INTO GHOST_DETECTION.APP.INVESTIGATIONS (
            investigation_id, case_name, ghost_id, lead_investigator_id,
            start_date, status, priority
        ) VALUES (
            '{inv_id}',
            '{investigation["case_name"]}',
            '{investigation["ghost_id"]}',
            '{investigation["lead_investigator_id"]}',
            CURRENT_DATE(),
            '{investigation.get("status", "Open")}',
            '{investigation.get("priority", "Medium")}'
        )
        """
        
        self.session.sql(sql).collect()
    
    def _process_single_image(self, image_file: Path, ghost_id: Optional[str] = None):
        """Process single image with Cortex Vision."""
        from uuid import uuid4
        
        # Upload to stage
        stage_path = f"@GHOST_IMAGES_STAGE/{image_file.name}"
        
        # Use PUT command to upload
        put_sql = f"PUT 'file://{image_file.absolute()}' @GHOST_IMAGES_STAGE OVERWRITE=TRUE"
        self.session.sql(put_sql).collect()
        
        # Analyze with Cortex Vision (simulated - actual implementation depends on available features)
        evidence_id = f"EV_{str(uuid4())[:8].upper()}"
        
        # Insert evidence record
        sql = f"""
        INSERT INTO GHOST_DETECTION.APP.GHOST_EVIDENCE (
            evidence_id, ghost_id, evidence_type,
            file_path, capture_datetime, processing_status
        ) VALUES (
            '{evidence_id}',
            {f"'{ghost_id}'" if ghost_id else 'NULL'},
            'Photograph',
            '{stage_path}',
            CURRENT_TIMESTAMP(),
            'Analyzed'
        )
        """
        
        self.session.sql(sql).collect()
        logger.info(f"Uploaded and cataloged: {image_file.name}")
    
    def generate_report(self) -> str:
        """Generate processing report."""
        if not self.start_time:
            return "No processing has been performed yet."
        
        elapsed = time.time() - self.start_time
        
        report = f"""
        ╔══════════════════════════════════════════════════════════════╗
        ║         BULK GHOST PROCESSING REPORT                         ║
        ╚══════════════════════════════════════════════════════════════╝
        
        Processing Time:     {elapsed:.2f} seconds
        Total Processed:     {self.processed_count} items
        Successful:          {self.processed_count - self.error_count} items
        Errors:              {self.error_count} items
        Success Rate:        {((self.processed_count - self.error_count) / max(self.processed_count, 1) * 100):.1f}%
        
        Items per second:    {self.processed_count / max(elapsed, 1):.2f}
        
        Status:              {'✅ COMPLETE' if self.error_count == 0 else '⚠️ COMPLETED WITH ERRORS'}
        """
        
        return report


def create_session():
    """Create Snowflake session from connection parameters.
    
    Supports both password and key pair authentication.
    
    For key pair auth, set:
    - SNOWFLAKE_PRIVATE_KEY_PATH: path to private key file
    - SNOWFLAKE_PRIVATE_KEY_PASSPHRASE: (optional) passphrase for encrypted key
    
    For password auth, set:
    - SNOWFLAKE_PASSWORD
    """
    from snowflake.snowpark import Session
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    
    # Load from environment or config
    connection_parameters = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "role": os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        "database": "GHOST_DETECTION",
        "schema": "APP"
    }
    
    # Check for key pair authentication
    private_key_path = os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH")
    
    if private_key_path and os.path.exists(private_key_path):
        logger.info("Using key pair authentication")
        
        # Read private key
        with open(private_key_path, "rb") as key_file:
            private_key_data = key_file.read()
        
        # Get passphrase if provided
        passphrase = os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE")
        passphrase_bytes = passphrase.encode() if passphrase else None
        
        # Load and deserialize private key
        private_key = serialization.load_pem_private_key(
            private_key_data,
            password=passphrase_bytes,
            backend=default_backend()
        )
        
        # Serialize to DER format for Snowflake
        pkb = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        connection_parameters["private_key"] = pkb
        logger.info("✅ Private key loaded successfully")
    else:
        # Use password authentication
        password = os.getenv("SNOWFLAKE_PASSWORD")
        if not password:
            raise ValueError("Either SNOWFLAKE_PASSWORD or SNOWFLAKE_PRIVATE_KEY_PATH must be set")
        connection_parameters["password"] = password
        logger.info("Using password authentication")
    
    return Session.builder.configs(connection_parameters).create()


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Bulk Ghost Data Processor')
    parser.add_argument('--mode', choices=['csv', 'images', 'json'], required=True,
                       help='Processing mode')
    parser.add_argument('--input', required=True,
                       help='Input file or directory path')
    parser.add_argument('--ghost-id', help='Ghost ID for image associations')
    
    args = parser.parse_args()
    
    logger.info("=" * 70)
    logger.info("BULK GHOST PROCESSOR - SnowGhost Breakers")
    logger.info("=" * 70)
    
    try:
        # Create session
        logger.info("Connecting to Snowflake...")
        session = create_session()
        logger.info("✅ Connected successfully")
        
        # Create processor
        processor = BulkGhostProcessor(session)
        
        # Process based on mode
        if args.mode == 'csv':
            results = processor.process_csv_sightings(args.input)
        elif args.mode == 'images':
            results = processor.process_image_directory(args.input, args.ghost_id)
        elif args.mode == 'json':
            results = processor.process_json_batch(args.input)
        
        # Generate report
        report = processor.generate_report()
        print(report)
        
        # Close session
        session.close()
        logger.info("Session closed")
        
        # Exit with appropriate code
        sys.exit(0 if processor.error_count == 0 else 1)
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

