import tkinter as tk
from tkinter import ttk, scrolledtext
import cv2
from PIL import Image, ImageTk
import torch
import threading
from transformers import AutoModelForCausalLM
from deepseek_vl2.models import DeepseekVLV2Processor
from deepseek_vl2.utils.io import load_pil_images

class CCTVMonitor:
    def __init__(self, root, model_path="deepseek-ai/deepseek-vl2-tiny"):
        self.root = root
        self.root.title("AI CCTV Monitor")
        
        # Initialize model
        self.model_path = model_path
        self.initialize_model()
        
        # Setup GUI
        self.setup_gui()
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.update_video()
        
    def initialize_model(self):
        self.processor = DeepseekVLV2Processor.from_pretrained(self.model_path)
        self.tokenizer = self.processor.tokenizer
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path, 
            trust_remote_code=True,
            device_map="auto"  # This will automatically use available hardware
        ).to(torch.bfloat16).eval()  # Remove .cuda()
        
    def setup_gui(self):
        # Video panel
        self.video_panel = ttk.Label(self.root)
        self.video_panel.grid(row=0, column=0, padx=10, pady=10)
        
        # Control panel
        control_frame = ttk.Frame(self.root)
        control_frame.grid(row=1, column=0, sticky='ew')
        
        self.process_btn = ttk.Button(
            control_frame, 
            text="Analyze Frame", 
            command=self.process_current_frame
        )
        self.process_btn.pack(side=tk.LEFT, padx=5)
        
        # Response area
        self.response_area = scrolledtext.ScrolledText(self.root, width=60, height=10)
        self.response_area.grid(row=2, column=0, padx=10, pady=10)
        
    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw green rectangle around face
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_panel.imgtk = imgtk
            self.video_panel.configure(image=imgtk)

            self.current_frame = frame  # Store frame for processing

        if self.running:
            self.root.after(10, self.update_video)

            
    def process_current_frame(self):
        self.process_btn.config(state=tk.DISABLED)
        threading.Thread(target=self.analyze_frame).start()
        
    def analyze_frame(self):
        try:
            # Convert frame to PIL Image
            pil_image = Image.fromarray(cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB))
            
            # Prepare conversation
            conversation = [{
                "role": "<|User|>",
                "content": "<image>\nDescribe any suspicious activity or objects in this CCTV frame.",
                "images": [pil_image]
            }, {"role": "<|Assistant|>", "content": ""}]
            
            # Process inputs
            pil_images = load_pil_images(conversation)
            prepare_inputs = self.processor(
                conversations=conversation,
                images=pil_images,
                force_batchify=True
            ).to(self.model.device)
            
            # Generate response
            inputs_embeds = self.model.prepare_inputs_embeds(**prepare_inputs)
            outputs = self.model.language.generate(
                inputs_embeds=inputs_embeds,
                attention_mask=prepare_inputs.attention_mask,
                pad_token_id=self.tokenizer.eos_token_id,
                bos_token_id=self.tokenizer.bos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                max_new_tokens=100,
                do_sample=False,
                use_cache=True
            )
            
            response = self.tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)
            self.display_response(response.split("<|Assistant|>:")[-1].strip())
            
        except Exception as e:
            self.display_response(f"Error: {str(e)}")
        finally:
            self.root.after(0, lambda: self.process_btn.config(state=tk.NORMAL))
            
    def display_response(self, text):
        self.response_area.config(state=tk.NORMAL)
        self.response_area.delete(1.0, tk.END)
        self.response_area.insert(tk.END, text + "\n")
        self.response_area.config(state=tk.DISABLED)
        
    def on_close(self):
        self.running = False
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CCTVMonitor(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()