#!/usr/bin/env python3
"""
Automated Installation Script for Ghost Detection System
Installs all components in the correct order
"""

import snowflake.connector
import os
from pathlib import Path
import sys
from getpass import getpass


class GhostDetectionInstaller:
    """Automated installer for Ghost Detection System"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.sql_files = [
            'sql/01_setup_database.sql',
            'sql/02_create_tables.sql',
            'sql/03_sample_data.sql',
            'sql/04_stored_procedures.sql',
            'sql/05_semantic_views.sql',
            'sql/06_cortex_ai_functions.sql',
            'sql/07_aisql_examples.sql',
            'sql/08_business_vocabulary.sql',
            'sql/09_agentic_ai_system.sql',
            'sql/10_snowflake_native_mcp_server.sql'
        ]
        self.connection = None
    
    def connect(self):
        """Connect to Snowflake"""
        print("\n" + "="*80)
        print("GHOST DETECTION SYSTEM - AUTOMATED INSTALLER")
        print("="*80)
        print("\nPlease provide your Snowflake connection details:\n")
        
        account = input("Snowflake Account (e.g., abc12345.us-east-1): ")
        user = input("Username: ")
        password = getpass("Password: ")
        warehouse = input("Warehouse (default: COMPUTE_WH): ") or "COMPUTE_WH"
        role = input("Role (default: ACCOUNTADMIN): ") or "ACCOUNTADMIN"
        
        try:
            print("\nConnecting to Snowflake...")
            self.connection = snowflake.connector.connect(
                account=account,
                user=user,
                password=password,
                warehouse=warehouse,
                role=role
            )
            print("✅ Connected successfully!")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def execute_sql_file(self, file_path):
        """Execute a SQL file"""
        full_path = self.project_root / file_path
        
        if not full_path.exists():
            print(f"❌ File not found: {file_path}")
            return False
        
        print(f"\n{'='*80}")
        print(f"Executing: {file_path}")
        print(f"{'='*80}")
        
        try:
            with open(full_path, 'r') as f:
                sql_content = f.read()
            
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            cursor = self.connection.cursor()
            
            for i, statement in enumerate(statements, 1):
                # Skip comments and empty statements
                if not statement or statement.startswith('--'):
                    continue
                
                try:
                    cursor.execute(statement)
                    result = cursor.fetchall()
                    
                    # Print results if any
                    if result:
                        for row in result[:5]:  # Print first 5 rows
                            print(f"  {row}")
                        if len(result) > 5:
                            print(f"  ... ({len(result)} total rows)")
                
                except Exception as e:
                    # Some statements might fail (e.g., IF NOT EXISTS)
                    # Only show critical errors
                    error_msg = str(e)
                    if "already exists" not in error_msg.lower():
                        print(f"⚠️  Statement {i}: {error_msg[:100]}")
            
            cursor.close()
            print(f"✅ Completed: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error executing {file_path}: {e}")
            return False
    
    def verify_installation(self):
        """Verify the installation"""
        print("\n" + "="*80)
        print("VERIFYING INSTALLATION")
        print("="*80)
        
        verification_queries = [
            ("Databases", "SHOW DATABASES LIKE 'GHOST_DETECTION'"),
            ("Tables", "SELECT COUNT(*) FROM GHOST_DETECTION.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'APP'"),
            ("Views", "SELECT COUNT(*) FROM GHOST_DETECTION.INFORMATION_SCHEMA.VIEWS WHERE TABLE_SCHEMA = 'ANALYTICS'"),
            ("Procedures", "SELECT COUNT(*) FROM GHOST_DETECTION.INFORMATION_SCHEMA.PROCEDURES WHERE PROCEDURE_SCHEMA = 'APP'"),
            ("Ghosts", "SELECT COUNT(*) FROM GHOST_DETECTION.APP.GHOSTS"),
            ("Sightings", "SELECT COUNT(*) FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS"),
            ("AI Agents", "SELECT COUNT(*) FROM GHOST_DETECTION.APP.AI_AGENTS"),
            ("MCP Servers", "SHOW MCP SERVERS IN DATABASE GHOST_DETECTION")
        ]
        
        cursor = self.connection.cursor()
        
        for name, query in verification_queries:
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                
                if "COUNT" in query:
                    count = result[0][0] if result else 0
                    print(f"✅ {name}: {count}")
                else:
                    count = len(result)
                    print(f"✅ {name}: {count} found")
            except Exception as e:
                print(f"⚠️  {name}: Could not verify ({str(e)[:50]})")
        
        cursor.close()
    
    def install(self):
        """Run the complete installation"""
        # Connect to Snowflake
        if not self.connect():
            return False
        
        # Execute all SQL files
        print("\n" + "="*80)
        print("INSTALLING COMPONENTS")
        print("="*80)
        
        success_count = 0
        for sql_file in self.sql_files:
            if self.execute_sql_file(sql_file):
                success_count += 1
        
        # Verify installation
        self.verify_installation()
        
        # Summary
        print("\n" + "="*80)
        print("INSTALLATION SUMMARY")
        print("="*80)
        print(f"Files Executed: {success_count}/{len(self.sql_files)}")
        
        if success_count == len(self.sql_files):
            print("\n✅ INSTALLATION COMPLETE!")
            print("\n🎉 Ghost Detection System is ready to use!")
            print("\nNext Steps:")
            print("  1. Review the main README.md")
            print("  2. Get OAuth credentials: SELECT SYSTEM$SHOW_OAUTH_CLIENT_SECRETS('GHOST_MCP_OAUTH');")
            print("  3. Deploy the Streamlit app")
            print("  4. Start catching ghosts! 👻")
        else:
            print("\n⚠️  Installation completed with warnings")
            print("Some components may not have been installed successfully.")
            print("Please review the output above and run failed scripts manually.")
        
        # Close connection
        if self.connection:
            self.connection.close()
        
        return success_count == len(self.sql_files)


def main():
    """Main entry point"""
    installer = GhostDetectionInstaller()
    
    try:
        success = installer.install()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

