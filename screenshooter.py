import tkinter as tk
from PIL import ImageGrab, Image, ImageTk
import io
import subprocess
from screeninfo import get_monitors

class ScreenCaptureApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.monitors = get_monitors()

        # Find the primary monitor
        primary_monitor = None
        for monitor in self.monitors:
            if monitor.is_primary:
                primary_monitor = monitor
                break

        # Move the primary monitor to the first position in the list
        if primary_monitor:
            self.monitors.remove(primary_monitor)
            self.monitors.insert(0, primary_monitor)

        # Thumbnail dimensions
        thumb_width = 300
        thumb_height = 200
        padding = 20  # Add some padding around the thumbnails

        # Calculate window size
        window_width = (thumb_width + padding) * len(self.monitors) + padding
        window_height = thumb_height + 2 * padding + 40  # Additional height for label

        # Create a selection window
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.title("Select Monitor")
        self.selection_window.geometry(f"{window_width}x{window_height}")

        label = tk.Label(self.selection_window, text="Select Monitor to Capture:")
        label.pack(pady=padding // 2)

        self.thumbnails = []
        for idx, monitor in enumerate(self.monitors):
            # Take a screenshot of each monitor for the thumbnail
            thumbnail = ImageGrab.grab(bbox=(monitor.x, monitor.y, monitor.width + monitor.x, monitor.height + monitor.y))
            thumbnail = thumbnail.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
            self.thumbnails.append(ImageTk.PhotoImage(thumbnail))

            button = tk.Button(self.selection_window, image=self.thumbnails[idx], command=lambda m=monitor: self.select_monitor(m))
            button.pack(side=tk.LEFT, padx=padding // 2, pady=padding // 2)

    def select_monitor(self, monitor):
        self.monitor = monitor
        self.selection_window.destroy()
        self.capture_screen()

    def capture_screen(self):
        # Wait for the selection window to close before capturing the screen
        self.root.after(200, self.capture_screen_after_delay)

    def capture_screen_after_delay(self):
        # Take a full-screen screenshot of the selected monitor
        self.full_screen_image = ImageGrab.grab(bbox=(self.monitor.x, self.monitor.y, self.monitor.width + self.monitor.x, self.monitor.height + self.monitor.y))

        self.top = tk.Toplevel(self.root)
        self.top.attributes("-fullscreen", True)
        self.top.attributes("-alpha", 0.0)  # Make the overlay completely transparent
        self.top.configure(bg="")

        self.canvas = tk.Canvas(self.top, cursor="cross", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Display the screenshot on the canvas
        self.image_tk = ImageTk.PhotoImage(self.full_screen_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_mouse_drag(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        bbox = (self.start_x, self.start_y, end_x, end_y)

        self.top.destroy()  # Destroy the overlay window
        self.root.update()  # Ensure all Tkinter events are processed

        if bbox[2] <= bbox[0] or bbox[3] <= bbox[1]:
            print("Invalid selection area")
            self.root.destroy()
            return

        # Wait for a short moment to ensure the overlay window is fully destroyed
        self.root.after(200, lambda: self.take_screenshot(bbox))

    def take_screenshot(self, bbox):
        # Crop the full-screen image using the bounding box
        img = self.full_screen_image.crop(bbox)

        # Convert the image to a format that can be used for clipboard
        output = io.BytesIO()
        img.save(output, format="PNG")
        data = output.getvalue()
        output.close()

        # Copy to clipboard (Linux specific method)
        self.copy_image_to_clipboard(data)
        print("Screenshot copied to clipboard.")

        self.root.destroy()

    def copy_image_to_clipboard(self, data):
        # Use xclip to copy the image to the clipboard on Linux
        process = subprocess.Popen(['xclip', '-selection', 'clipboard', '-t', 'image/png'], stdin=subprocess.PIPE)
        process.stdin.write(data)
        process.stdin.close()
        process.wait()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ScreenCaptureApp()
    app.run()
