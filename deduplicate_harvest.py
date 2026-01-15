import re
import os

f_path = 'knowledge_harvester_append/master_harvest.html'

def fix_duplicates():
    if not os.path.exists(f_path):
        print("File not found.")
        return

    with open(f_path, 'r', encoding='utf-8') as f:
        c = f.read()

    # Split by ENTRY_START markers while capturing them
    # The regex group () keeps the delimiter in the result list
    parts = re.split(r'(<!-- ENTRY_START_[a-f0-9\-]+ -->)', c)
    
    # parts[0] is everything BEFORE the first entry (header, styles, scripts)
    final_content = parts[0]
    seen_ids = set()
    
    # The split results in: [preamble, marker1, body1, marker2, body2, ...]
    # So we iterate starting from index 1 in steps of 2
    count_removed = 0
    
    for i in range(1, len(parts), 2):
        marker = parts[i]
        body = parts[i+1] # This contains the entry content + END marker + any whitespace after
        
        # Extract ID
        # Marker format: <!-- ENTRY_START_uuid-uuid... -->
        eid = marker.replace('<!-- ENTRY_START_', '').replace(' -->', '')
        
        if eid not in seen_ids:
            final_content += marker + body
            seen_ids.add(eid)
        else:
            print(f"Removing Duplicate Entry: {eid}")
            count_removed += 1

    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"Cleanup Complete. Removed {count_removed} duplicates.")

if __name__ == "__main__":
    fix_duplicates()
