from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SMTP Configuration ---
SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587
SMTP_USERNAME = "asutosh@accrosian.com"
SMTP_PASSWORD = "Accrosian@#123"  # Replace with your Hostinger password

# --- Request Model ---
class Applicant(BaseModel):
    name: str
    email: EmailStr

# --- Email Function ---
def send_email(name: str, to_email: str):
    # Achievement-focused subject line
    subject = f"🎉 Congratulations {name}! You’re On Your Way to a Big Opportunity!"

    # Short, attractive HTML email body
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">

        <!-- Header -->
        <div style="background-color: #f0f8ff; padding: 15px; text-align: center; border-radius: 8px;">
          <h2 style="color: #2e86de;">🎉 Congratulations {name}!</h2>
          <p style="margin: 0; font-size: 16px;">You’re On Your Way to a Big Opportunity!</p>
        </div>

        <hr style="border: 0; border-top: 1px solid #ddd; margin: 20px 0;">

        <!-- Body Content -->
        <p>Hi <b>{name}</b> 👋,</p>

        <p>🌟 Welcome as a <b>Strategic Partner</b>! This is a great chance to <b>gain experience</b> and <b>boost your professional profile</b>. 🏆</p>

        <p>🚀 Get ready to take your first step toward achieving something big!</p>

        <p>Our team will <b>touch with you shortly</b>. 💼</p>

        <hr style="border: 0; border-top: 1px solid #ddd; margin: 20px 0;">

        <div style="text-align:center; line-height:1.5;">
        Best regards,<br>
        <strong>Asutosh</strong><br>
        🌟 Accrosian Team 🌟
        </div>
      </body>
    </html>
    """

    try:
        # Create MIME message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = "Accrosian Team <asutosh@accrosian.com>"
        msg["To"] = to_email
        msg.attach(MIMEText(html_body, "html"))

        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        server.quit()

        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# --- Webhook Endpoint ---
@app.post("/webhook")
async def webhook(applicant: Applicant):
    success = send_email(applicant.name, applicant.email)
    if success:
        return {"status": "success", "message": f"Email sent to {applicant.email}"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")
