import gradio as gr
import requests
import json

API_URL = "http://localhost:8000/analyze"
HISTORY_URL = "http://localhost:8000/complaints"

def analyze_complaint(image, complaint_text):
    if image is None:
        return "Please upload a product image."
    
    if not complaint_text:
        return "Please describe your complaint."
    
    try:
        with open(image, "rb") as img_file:
            files = {"image": img_file}
            data = {"complaint": complaint_text}
            
            response = requests.post(
                API_URL,
                files=files,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                source = result.get("source", "ai")
                ai_response = result.get("response", "")
                
                source_label = "⚡ Cached Response" if source == "cache" else "🤖 AI Response"
                
                return f"{source_label}\n\n{ai_response}"
            else:
                return f"Error: {response.status_code}"
                
    except Exception as e:
        return f"Error connecting to API: {str(e)}"

def get_complaint_history():
    try:
        response = requests.get(HISTORY_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            complaints = data.get("complaints", [])
            total = data.get("total", 0)
            
            if not complaints:
                return "No complaints yet."
            
            history = f"Total Complaints: {total}\n\n"
            for c in complaints[-5:]:
                history += f"ID: {c['id']}\n"
                history += f"Complaint: {c['complaint']}\n"
                history += f"Status: {c['status']}\n"
                history += f"Time: {c['created_at']}\n"
                history += "-" * 50 + "\n"
            
            return history
    except:
        return "Could not fetch history."

# Build Gradio UI
with gr.Blocks(title="AI Customer Support Agent", theme=gr.themes.Soft()) as app:
    
    gr.Markdown("""
    # 🤖 AI Customer Support Agent
    ### Upload a product image and describe your complaint
    *Powered by GPT-4V — Multimodal AI*
    """)
    
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(
                type="filepath",
                label="📸 Upload Product Image"
            )
            complaint_input = gr.Textbox(
                label="📝 Describe Your Complaint",
                placeholder="Example: I received a damaged product. The screen is cracked.",
                lines=4
            )
            submit_btn = gr.Button(
                "🚀 Analyze Complaint",
                variant="primary"
            )
        
        with gr.Column():
            response_output = gr.Textbox(
                label="🤖 AI Response",
                lines=12,
                interactive=False
            )
    
    gr.Markdown("---")
    
    with gr.Row():
        history_btn = gr.Button("📋 View Complaint History")
        history_output = gr.Textbox(
            label="Complaint History",
            lines=10,
            interactive=False
        )
    
    submit_btn.click(
        fn=analyze_complaint,
        inputs=[image_input, complaint_input],
        outputs=response_output
    )
    
    history_btn.click(
        fn=get_complaint_history,
        inputs=[],
        outputs=history_output
    )
    
    gr.Markdown("""
    ### How it works:
    1. Upload a photo of your damaged/wrong product
    2. Describe your complaint in text
    3. AI analyzes BOTH image and text together
    4. Get an instant resolution response
    """)

if __name__ == "__main__":
    app.launch(server_port=7860, share=False)