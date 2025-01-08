import sqlite3
import json

def initialize_database(db_name):
    """Initialize the SQLite database and create the table."""
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS channels (
        channel_id TEXT PRIMARY KEY,
        channel_name TEXT NOT NULL,
        videos TEXT
    )
    ''')
    
    connection.commit()
    connection.close()

def create_channel(db_name, channel_id, channel_name, videos=None):
    """Create a new channel record."""
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    
    videos_json = json.dumps(videos or [])  # Convert videos list to JSON string, default to empty list if None
    try:
        cursor.execute('''
        INSERT INTO channels (channel_id, channel_name, videos)
        VALUES (?, ?, ?)
        ''', (channel_id, channel_name, videos_json))
        connection.commit()
    except sqlite3.IntegrityError:
        print(f"Error: Channel with ID '{channel_id}' already exists.")
    finally:
        connection.close()

def read_channel(db_name, channel_id):
    """Read a channel record by its ID."""
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    
    cursor.execute('''
    SELECT * FROM channels WHERE channel_id = ?
    ''', (channel_id,))
    result = cursor.fetchone()
    connection.close()
    
    if result:
        return {
            "channel_id": result[0],
            "channel_name": result[1],
            "videos": json.loads(result[2])  # Convert JSON string back to list
        }
    else:
        print(f"Channel with ID '{channel_id}' not found.")
        return None

def update_channel(db_name, channel_id,  videos=None):
    """Update a channel record."""
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    
    if videos is not None:
        videos_json = json.dumps(videos)
        cursor.execute('''
        UPDATE channels
        SET videos = ?
        WHERE channel_id = ?
        ''', (videos_json, channel_id))
    
    connection.commit()
    connection.close()

def delete_channel(db_name, channel_id):
    """Delete a channel record by its ID."""
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    
    cursor.execute('''
    DELETE FROM channels WHERE channel_id = ?
    ''', (channel_id,))
    connection.commit()
    connection.close()

def list_channel_ids(db_name):
    """Get a list of all channel IDs in the database."""
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    
    cursor.execute('''
    SELECT channel_id FROM channels
    ''')
    result = cursor.fetchall()
    connection.close()
    
    return [row[0] for row in result]

# Example usage:
if __name__ == "__main__":
    db_name = "channelsVideoData.db"
    initialize_database(db_name)

    # Create a channel
    create_channel(db_name, "UCt7esZt_MwWXl9fgT0yO1eA", "Drake on Digital ")
    create_channel(db_name, "UCbLhGKVY-bJPcawebgtNfbw", "Altcoin Daily")
    # Read the channel
    print(read_channel(db_name, "UCbLhGKVY-bJPcawebgtNfbw"))
    print(read_channel(db_name, "UCt7esZt_MwWXl9fgT0yO1eA"))

    # Update the channel
    # videos = ["Video3", "Video4"]
    # update_channel(db_name, "1", videos)

    # Read the updated channel
    # print(read_channel(db_name, "1")['videos'])

    # List all channel IDs
    print(list_channel_ids(db_name))

    # Delete the channel
    # delete_channel(db_name, "1")

    # Try reading the deleted channel
    # print(read_channel(db_name, "2"))
