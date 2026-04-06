import uvicorn
import os

from app.config import is_development

if __name__ == "__main__":
  
  host = os.getenv("HOST", "127.0.0.1")
  port = int(os.getenv("PORT", "8000"))
  reload = is_development()
    
  print(f"Starting server at http://{host if host != '0.0.0.0' else 'localhost'}:{port}")
    
  uvicorn.run(
      "app.main:app",
      host=host,
      port=port,
      reload=reload
  )