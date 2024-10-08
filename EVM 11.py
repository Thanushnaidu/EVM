import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk, ImageSequence
import tkinter.font as font
import re
import os

class VotingSystemApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Electronic Voting System")
        self.root.geometry("900x700")  # Main window size
        self.root.configure(bg="#f8f9fa")
        self.root.withdraw()  # Hide the main Tkinter window

        # Initialize vote counts and used IDs
        self.vote_counts = {
            "KONIDELA PAWAN KALYAN  ": 0,
            "NARA CHANDRABABU NAIDU": 0,
            "Y S JAGAN MOHAN REDDY      ": 0
        }
        self.used_ids = set()  # To track used voter IDs

        # Load custom fonts
        self.title_font = font.Font(family="Times New Roman", size=18, weight="bold", slant="roman", underline=False)
        self.button_font = font.Font(family="Times New Roman", size=13, weight="normal", slant="roman", underline=False)

        # Load images (Ensure these paths are correct and accessible)
        self.candidate_symbols = {
            "KONIDELA PAWAN KALYAN  ": ImageTk.PhotoImage(Image.open(r"glass.png").resize((40, 40))),
            "NARA CHANDRABABU NAIDU": ImageTk.PhotoImage(Image.open(r"cycle.png").resize((40, 40))),
            "Y S JAGAN MOHAN REDDY      ": ImageTk.PhotoImage(Image.open(r"fan.png").resize((40, 40)))
        }

        self.candidate_images = {
            "KONIDELA PAWAN KALYAN  ": ImageTk.PhotoImage(Image.open(r"pawan3.png").resize((50, 50))),
            "NARA CHANDRABABU NAIDU": ImageTk.PhotoImage(Image.open(r"cbn.png").resize((50, 50))),
            "Y S JAGAN MOHAN REDDY      ": ImageTk.PhotoImage(Image.open(r"jagan.png").resize((50, 50)))
        }

        # Arrow image to indicate voting button
        self.arrow_image = ImageTk.PhotoImage(Image.open(r"arrow.png").resize((30, 30)))

        # Initialize windows
        self.user_confirmation_window = None
        self.voting_window = None
        self.confirmation_window = None
        self.success_window = None
        self.results_window = None
        self.ec_login_window = None  # Initialize ec_login_window here

        # GIF animation attributes
        self.gif_frames = []
        self.current_gif_frame = 0
        self.gif_label = None

        # Show User Confirmation Window
        self.show_user_confirmation_window()

    def show_user_confirmation_window(self):
        # Close any existing window before opening a new one
        if self.user_confirmation_window:
            self.user_confirmation_window.destroy()

        self.user_confirmation_window = tk.Toplevel(self.root)
        self.user_confirmation_window.title("User Confirmation")
        self.user_confirmation_window.geometry("900x700")  # Adjusted size
        self.user_confirmation_window.configure(bg="white")

        # Set up video background
        self.video_path = r"BG 8.mp4"
        self.video_label = tk.Label(self.user_confirmation_window)
        self.video_label.place(relwidth=1, relheight=1)

        # Load and play video
        if os.path.exists(self.video_path):
            self.video_capture = cv2.VideoCapture(self.video_path)
            self.update_video_frame()
        else:
            messagebox.showerror("Video Error", f"Video file not found at {self.video_path}")

        # Buttons for Voter Details and EC Login
        voter_button = tk.Button(self.user_confirmation_window, text="Voter Login", command=self.show_voter_details_window,
                                 font=self.button_font, bg="#007bff", fg="white", relief="raised", width=20, height=2)
        voter_button.place(relx=0.29, rely=0.42, anchor="center")

        ec_login_button = tk.Button(self.user_confirmation_window, text="EC Login", command=self.show_ec_login_window,
                                    font=self.button_font, bg="#28a745", fg="white", relief="raised", width=20, height=2)
        ec_login_button.place(relx=0.68, rely=0.42, anchor="center")

    def show_voter_details_window(self):
        # Voter Details Window (Entry for Voter ID)
        if self.voting_window:
            self.voting_window.destroy()

        self.voting_window = tk.Toplevel(self.root)
        self.voting_window.title("Voter Details")
        self.voting_window.geometry("600x400")
        self.voting_window.configure(bg="white")

        # Heading for Voter Details
        tk.Label(self.voting_window, text="Enter Voter ID", font=self.title_font, bg="white", fg="black").pack(pady=20)
        
        self.voter_id_var = tk.StringVar()
        self.voter_id_entry = tk.Entry(self.voting_window, textvariable=self.voter_id_var, font=self.button_font, width=30, bg="white")
        self.voter_id_entry.pack(pady=10)

        # Submit Button for Voter ID
        tk.Button(self.voting_window, text="Submit", command=self.verify_voter_id, font=self.button_font, bg="#007bff", fg="white", relief="flat", width=15, height=2).pack(pady=20)

    def show_voter_details_window(self):
        # Voter Details Window (Entry for Voter ID)
        if self.voting_window:
            self.voting_window.destroy()

        self.voting_window = tk.Toplevel(self.root)
        self.voting_window.title("Voter Details")
        self.voting_window.geometry("600x400")
        self.voting_window.configure(bg="white")

        # Heading for Voter Details
        tk.Label(self.voting_window, text="Enter Voter ID", font=self.title_font, bg="white", fg="black").pack(pady=20)
        
        self.voter_id_var = tk.StringVar()
        self.voter_id_entry = tk.Entry(self.voting_window, textvariable=self.voter_id_var, font=self.button_font, width=30, bg="white")
        self.voter_id_entry.pack(pady=10)

        # Submit Button for Voter ID
        tk.Button(self.voting_window, text="Submit", command=self.verify_voter_id, font=self.button_font, bg="#007bff", fg="white", relief="flat", width=15, height=2).pack(pady=20)

    def show_ec_login_window(self):
        # EC Login Window (Entry for EC Code)
        if self.ec_login_window:
            self.ec_login_window.destroy()

        self.ec_login_window = tk.Toplevel(self.root)
        self.ec_login_window.title("EC Login")
        self.ec_login_window.geometry("600x400")
        self.ec_login_window.configure(bg="white")

        # Heading for EC Login
        tk.Label(self.ec_login_window, text="Enter EC Code", font=self.title_font, bg="white", fg="black").pack(pady=20)

        self.ec_credentials_var = tk.StringVar()
        self.ec_credentials_entry = tk.Entry(self.ec_login_window, textvariable=self.ec_credentials_var, font=self.button_font, show="*", width=30, bg="white")
        self.ec_credentials_entry.pack(pady=10)

        # Submit Button for EC Code
        tk.Button(self.ec_login_window, text="Submit", command=self.verify_ec_credentials, font=self.button_font, bg="#28a745", fg="white", relief="flat", width=15, height=2).pack(pady=20)

    def update_video_frame(self):
        ret, frame = self.video_capture.read()
        if not ret:
            # Restart the video when it ends
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.video_capture.read()
        if ret:
            # Resize the frame to fit the window
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.user_confirmation_window.winfo_width(), self.user_confirmation_window.winfo_height()))
            frame_image = Image.fromarray(frame)
            frame_image = ImageTk.PhotoImage(frame_image)
            self.video_label.config(image=frame_image)
            self.video_label.image = frame_image
        self.video_label.after(30, self.update_video_frame)

    def verify_voter_id(self):
        voter_id = self.voter_id_var.get().strip()
        if self.is_valid_voter_id(voter_id):
            if voter_id in self.used_ids:
                messagebox.showerror("Error", "This Voter ID has already been used.")
            else:
                self.used_ids.add(voter_id)
                self.show_voting_window()
        else:
            messagebox.showerror("Error", "Invalid Voter ID. Please enter a 10-digit number.")

    def verify_ec_credentials(self):
        ec_code = self.ec_credentials_var.get().strip()
        if ec_code == "THANUSH NAIDU":
            self.show_results_window()
        else:
            messagebox.showerror("Error", "Invalid EC Code. Access Denied.")

    def is_valid_voter_id(self, voter_id):
        return re.match(r'^\d{10}$', voter_id) is not None

    def show_voting_window(self):
        # Close any existing voting window before opening a new one
        if self.voting_window:
            self.voting_window.destroy()

        self.voting_window = tk.Toplevel(self.root)
        self.voting_window.title("Voting")
        self.voting_window.geometry("1000x1000")  # Adjusted size
        self.voting_window.configure(bg="#f8f9fa")

        # Load and display heading image
        heading_image_path = r"eci heading.png"
        try:
            heading_image = Image.open(heading_image_path)
            heading_image = ImageTk.PhotoImage(heading_image.resize((1000, 100)))
            heading_label = tk.Label(self.voting_window, image=heading_image, bg="#f8f9fa")
            heading_label.image = heading_image  # Keep a reference
            heading_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load heading image: {e}")

        # Title Label
        tk.Label(self.voting_window, text="Vote for Your Candidate", font=self.title_font, bg="#f8f9fa", fg="#343a40").pack(pady=20)

        # Candidate Frames
        for candidate, symbol_image in self.candidate_symbols.items():
            candidate_frame = tk.Frame(self.voting_window, bg="white", relief="solid", borderwidth=1)
            candidate_frame.pack(padx=10, pady=10, fill="x", expand=False)

            # Add candidate image
            candidate_image = self.candidate_images[candidate]
            tk.Label(candidate_frame, image=candidate_image, bg="white").grid(row=0, column=0, padx=20, pady=10)

            # Add candidate name
            tk.Label(candidate_frame, text=candidate, font=self.button_font, bg="white", fg="black").grid(row=0, column=1, padx=42, pady=10, sticky="w")

            # Add symbol image
            tk.Label(candidate_frame, image=symbol_image, bg="white").grid(row=0, column=2, padx=64, pady=10)

            # Add vote button with arrow
            vote_button = tk.Button(candidate_frame, text="Vote", font=self.button_font, bg="#A9A9A9", fg="black", relief="sunken",
                                    command=lambda c=candidate: self.confirm_vote(c), width=10, height=2)
            vote_button.grid(row=0, column=4, padx=76, pady=10)

            arrow_label = tk.Label(candidate_frame, image=self.arrow_image, bg="white")
            arrow_label.grid(row=0, column=3, padx=89, pady=10)

    def confirm_vote(self, candidate):
        # Open a custom confirmation window
        self.confirmation_window = tk.Toplevel(self.root)
        self.confirmation_window.title("Confirm Vote")
        self.confirmation_window.geometry("400x200")
        self.confirmation_window.configure(bg="white")

        # Confirmation message
        tk.Label(self.confirmation_window, text=f"Are you sure you want to vote for {candidate}?", font=self.title_font, bg="white", fg="black", wraplength=380).pack(pady=20)

        # Buttons Frame
        buttons_frame = tk.Frame(self.confirmation_window, bg="white")
        buttons_frame.pack(pady=10)

        # Yes Button
        yes_button = tk.Button(buttons_frame, text="Yes", command=lambda: self.cast_vote(candidate), font=self.button_font, bg="#28a745", fg="white", relief="flat", width=10, height=2)
        yes_button.pack(side="left", padx=20)

        # Cancel Button
        cancel_button = tk.Button(buttons_frame, text="Cancel", command=self.confirmation_window.destroy, font=self.button_font, bg="#dc3545", fg="white", relief="flat", width=10, height=2)
        cancel_button.pack(side="right", padx=20)

    def cast_vote(self, candidate):
        self.vote_counts[candidate] += 1
        # Show success window
        self.show_success_window()
        # Destroy the voting window and confirmation window
        if self.confirmation_window:
            self.confirmation_window.destroy()
        if self.voting_window:
            self.voting_window.destroy()

    def show_success_window(self):
        self.success_window = tk.Toplevel(self.root)
        self.success_window.title("Vote Casted")
        self.success_window.geometry("700x800")
        self.success_window.configure(bg="white")

        # Load and display GIF
        gif_path = r"TICK.gif"
        if os.path.exists(gif_path):
            try:
                gif_image = Image.open(gif_path)
                self.gif_frames = [ImageTk.PhotoImage(frame.copy().resize((100, 100))) for frame in ImageSequence.Iterator(gif_image)]
                self.current_gif_frame = 0

                self.gif_label = tk.Label(self.success_window, bg="white")
                self.gif_label.pack(pady=20)
                self.update_gif_frame()
            except Exception as e:
                messagebox.showerror("GIF Error", f"Failed to load GIF: {e}")
        else:
            messagebox.showerror("GIF Error", f"GIF file not found at {gif_path}")

        # Success message
        tk.Label(self.success_window, text="YOUR VOTE HAS BEEN SUCCESSFULLY CASTED.\nTHANK YOU.", font=self.title_font, bg="white", fg="green", justify="center").pack(pady=20)

        # Close Button
        close_button = tk.Button(self.success_window, text="Close", command=self.close_success_window, font=self.button_font, bg="#007bff", fg="white", relief="flat", width=10, height=2)
        close_button.pack(pady=10)

    def update_gif_frame(self):
        if self.gif_frames:
            frame = self.gif_frames[self.current_gif_frame]
            self.gif_label.config(image=frame)
            self.current_gif_frame = (self.current_gif_frame + 1) % len(self.gif_frames)
            self.gif_label.after(100, self.update_gif_frame)  # Adjust the delay as needed

    def close_success_window(self):
        if self.success_window:
            self.success_window.destroy()
        # Redirect to the main user confirmation window
        self.show_user_confirmation_window()

    def show_results_window(self):
        # Close any existing window before opening a new one
        if self.results_window:
            self.results_window.destroy()

        self.results_window = tk.Toplevel(self.root)
        self.results_window.title("Election Results")
        self.results_window.geometry("800x600")
        self.results_window.configure(bg="white")

        # Heading for Results Window
        tk.Label(self.results_window, text="Election Results", font=self.title_font, bg="white", fg="black").pack(pady=20)

        results_frame = tk.Frame(self.results_window, bg="white")
        results_frame.pack(pady=10)

        # Displaying the results
        for candidate, count in self.vote_counts.items():
            candidate_result = tk.Label(results_frame, text=f"{candidate}: {count} votes", font=self.title_font, bg="white", fg="black")
            candidate_result.pack(pady=10)

        close_button = tk.Button(self.results_window, text="Close", command=self.results_window.destroy, font=self.button_font, bg="#007bff", fg="white", relief="flat", width=10, height=2)
        close_button.pack(pady=20)

if __name__ == "__main__":
    app = VotingSystemApp()
    app.root.mainloop()
