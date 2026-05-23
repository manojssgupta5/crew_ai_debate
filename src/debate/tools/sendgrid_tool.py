import os
from crewai.tools import BaseTool
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class SendGridEmailTool(BaseTool):
    name: str = "SendGrid Email Tool"
    description: str = "Send emails using SendGrid"

    def _run(self, to_email: str, subject: str, body: str) -> str:
        try:
            sender_email = os.getenv("EMAIL_ADDRESS")
            to_email = os.getenv("EMAIL_ADDRESS")
            sendgrid_api_key = os.getenv("SENDGRID_API_KEY")

            if not sender_email:
                raise ValueError("send EMAIL_ADDRESS environment variable is missing")
            if not to_email:
                raise ValueError("receive EMAIL_ADDRESS environment variable is missing")
            if not sendgrid_api_key:
                raise ValueError("SENDGRID_API_KEY environment variable is missing")

            message = Mail(
                from_email=sender_email, 
                to_emails=to_email,
                subject=subject, 
                plain_text_content=body
            )
            sg = SendGridAPIClient(sendgrid_api_key)
            response = sg.send(message)
            return f"Email sent successfully with status {response.status_code}"

        except Exception as e:
            raise RuntimeError(f"SendGrid email failed: {str(e)}") from e