import simple_render_capture
import os

print("🚀 Saving clipboard content...")
filepath = simple_render_capture.save_from_clipboard()

if filepath:
    print(f"🎉 Opening {filepath}...")
    os.system(f'start "" "{filepath}"')
