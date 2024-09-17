import struct

def parse_git_index(data):
    # Parse header
    signature, version, num_entries = struct.unpack('>4sII', data[:12])
    
    if signature != b'DIRC':
        raise ValueError("Invalid index file signature")

    print(f"Signature: {signature.decode()}")
    print(f"Version: {version}")
    print(f"Number of Entries: {num_entries}")

    offset = 12
    entries = []
    for _ in range(num_entries):
        # Parse entry
        entry_data = data[offset:offset+62]  # Initial 62 bytes of entry
        ctime_s, ctime_n, mtime_s, mtime_n, dev, ino, mode, uid, gid, size = struct.unpack('>10I', entry_data[:40])
        sha1 = entry_data[40:60].hex()
        flags = struct.unpack('>H', entry_data[60:62])[0]
        name_length = flags & 0xFFF
        
        # Read file path (variable length, null-terminated)
        name_offset = offset + 62
        name_end = data.find(b'\x00', name_offset)
        name = data[name_offset:name_end].decode()
        
        # Calculate the entry's length in the file, including padding
        entry_len = 62 + len(name) + 1  # +1 for null terminator
        entry_len = (entry_len + 8) & ~7  # Align to the next multiple of 8

        # Add the parsed entry to the list
        entries.append({
            'ctime': (ctime_s, ctime_n),
            'mtime': (mtime_s, mtime_n),
            'dev': dev,
            'ino': ino,
            'mode': mode,
            'uid': uid,
            'gid': gid,
            'size': size,
            'sha1': sha1,
            'flags': flags,
            'name': name,
        })

        # Move to the next entry
        offset += entry_len

    return entries

data = open(".git/index", "rb").read()

# Parse the data
entries = parse_git_index(data)

# Output the parsed entries
for i, entry in enumerate(entries):
    print(f"\nEntry {i + 1}:")
    for key, value in entry.items():
        print(f"  {key}: {value}")
