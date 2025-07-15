#!/usr/bin/env python3
"""
Database Recovery Script
This script helps recover from the database corruption issue where
the classes_studentclass table has invalid foreign key values.
"""

import sqlite3
import os
import sys

def check_database_corruption(db_path):
    """Check if the database has the corruption issue"""
    if not os.path.exists(db_path):
        print(f"Database file {db_path} does not exist.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the problematic table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='classes_studentclass'")
        if not cursor.fetchone():
            print("Table classes_studentclass does not exist.")
            conn.close()
            return False
        
        # Check for the specific corruption
        cursor.execute("SELECT user_id FROM classes_studentclass WHERE user_id = 'user_id'")
        corrupted_rows = cursor.fetchall()
        conn.close()
        
        if corrupted_rows:
            print(f"Found {len(corrupted_rows)} corrupted rows with literal 'user_id' string.")
            return True
        else:
            print("No corruption found - database appears clean.")
            return False
            
    except Exception as e:
        print(f"Error checking database: {e}")
        return False

def fix_database_corruption(db_path):
    """Fix the database corruption by removing invalid rows"""
    if not os.path.exists(db_path):
        print(f"Database file {db_path} does not exist.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Delete rows with invalid user_id
        cursor.execute("DELETE FROM classes_studentclass WHERE user_id = 'user_id'")
        deleted_count = cursor.rowcount
        
        # Also clean up any other non-numeric user_id values
        cursor.execute("DELETE FROM classes_studentclass WHERE user_id NOT GLOB '[0-9]*'")
        deleted_count += cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"Fixed database - removed {deleted_count} corrupted rows.")
        return True
        
    except Exception as e:
        print(f"Error fixing database: {e}")
        return False

def main():
    # Default database path for Django projects
    db_path = "db.sqlite3"
    
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    
    print(f"Checking database: {db_path}")
    
    if check_database_corruption(db_path):
        response = input("Database corruption detected. Do you want to fix it? (y/N): ")
        if response.lower() in ['y', 'yes']:
            if fix_database_corruption(db_path):
                print("Database fixed successfully!")
                print("You can now try running 'python manage.py migrate' again.")
            else:
                print("Failed to fix database.")
        else:
            print("Database not fixed. Consider backing up your database and starting fresh.")
    
if __name__ == "__main__":
    main()